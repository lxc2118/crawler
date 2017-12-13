#!/usr/bin/env python
# coding=utf-8
import json
import logging

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

log_format = '%(asctime)s %(filename)s[line:%(lineno)d]'\
    + ' %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=log_format,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/usr/local/nagios/var/realtime.log',
                    filemode='w')


class LocalConnection(object):
    def __init__(self, stream):
        self.stream = stream
        self.stream.set_close_callback(self.on_close)
        self.read_message()

    def read_message(self):
        self.stream.read_until("\n", self.handle_message)

    def handle_message(self, msg):
        msg = msg[:-1]
        if msg == "query":
            result = self.get_result()
            self.write_message(result)
        self.read_message()

    def write_message(self, data):
        self.stream.write(data)

    def _fit_unit(self, data):
        unit_lv = 0
        result = float(data)
        for i in range(1, 4):
            if result >= 1024:
                result = result / 1024
                unit_lv = unit_lv + 1
            else:
                break

        unit = 'KB'
        if unit_lv == 1:
            unit = 'MB'
        if unit_lv == 2:
            unit = 'GB'
        if unit_lv == 3:
            unit = 'TB'
        return '%.2f %s' % (result, unit)

    def get_result(self):
        cpu_used = 0
        cpu_num = 0
        mem_used = 0
        mem_total = 0
        disk_used = 0
        disk_total = 0
        net_up = 0
        net_down = 0
        for client in Connection.clients:
            data = getattr(client, "resource_data", None)
            if data is None:
                continue
            item = json.loads(data)
            cpu_used = cpu_used + float(item["cpu"]["usage"])
            cpu_num = cpu_num + float(item["cpu"]["num"])
            mem_used = mem_used + float(item["mem"]["used"])
            mem_total = mem_total + float(item["mem"]["total"])
            disk_used = disk_used + float(item["disk"]["used"])
            disk_total = disk_total + float(item["disk"]["total"])
            net_up = net_up + float(item["net"]["up"])
            net_down = net_down + float(item["net"]["down"])

        if cpu_num == 0:
            return "None"
        cpu_usage = int(cpu_used / cpu_num * 100)
        mem_usage = int(mem_used / mem_total * 100)
        disk_usage = int(disk_used / disk_total * 100)
        cpu = {"usage": cpu_usage,
               "used": round(cpu_used, 2),
               "total": round(cpu_num, 2), }
        mem = {"usage": mem_usage,
               "used": self._fit_unit(mem_used),
               "total": self._fit_unit(mem_total), }
        disk = {"usage": disk_usage,
                "used": self._fit_unit(disk_used),
                "total": self._fit_unit(disk_total), }
        net = {"upload": round(net_up / 1024, 2),
               "download": round(net_down / 1024, 2), }
        result = {"cpu": cpu,
                  "mem": mem,
                  "disk": disk,
                  "net": net, }

        return json.dumps(result)

    def on_close(self):
        Connection.stop_monitor()


class Connection(object):
    clients = set()

    def __init__(self, stream, address):
        Connection.clients.add(self)
        self.stream = stream
        self.address = address
        # db_file = "/usr/local/nagios/realtime_monitor.db"
        # self.conn, self.cur = db.init_connection(db_file)
        self.stream.set_close_callback(self.on_close)
        self.read_message()

    @classmethod
    def stop_monitor(cls):
        for client in cls.clients:
            logging.info("Close client " + client.address[0])
            client.stream.write("stop")

    def read_message(self):
        self.stream.read_until("\n", self._update_database)

    def _update_database(self, data):
        data = data[:-1]
        try:
            json.loads(data)
            flag = True
        except:
            flag = False
        if flag:
            self.resource_data = data
            # value_dict = {"data": "'%s'" % data, }
            # conditon = {"ip": "'%s'" % self.address[0]}
            # db.update_or_insert(self.conn, self.cur, "resources",
            #                     value_dict, conditon)
        self.read_message()

    def on_close(self):
        Connection.clients.remove(self)
        logging.info("Close connection:" + self.address[0])
        # db.close_connection(self.conn, self.cur)


class MonitorLinuxServer(TCPServer):
    def handle_stream(self, stream, address):
        logging.info("New connection:" + address[0])
        if address[0] == "127.0.0.1":
            logging.info("Begin local monitor")
            # logging.info("Begin to stop realtime monitor client!")
            LocalConnection(stream)
            # Connection.stop_monitor()
        else:
            Connection(stream, address)


if __name__ == "__main__":
    logging.info("server start....")
    server = MonitorLinuxServer()
    port = 8000
    server.listen(port)
    IOLoop.instance().start()
