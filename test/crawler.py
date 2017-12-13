import urllib
import urllib2
import os

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/62.0.3202.75 Safari/537.36",
}

REQUEST_DATA = {
    'name': 'Michael Foord',
    'age': '18',
}

URL = "http://www.baidu.com"


def mk_file(path):
    if not os.path.exists(path):
        if path.endswith("/"):
            os.makedirs(path)
        else:
            dir_path = path[:path.rfind("/")]
            if os.path.exists(dir_path):
                os.makedirs(dir_path)
            os.mknod(file)


if __name__ == "__main__":
    hyps = []
    for v in [[1],[2],[3]]:
        print v
        hyps.extend(v)
    pass
    # data = urllib.urlencode(REQUEST_DATA)
    # print data
    # req = urllib2.Request(URL, headers=REQUEST_HEADERS)
    # resp = urllib2.urlopen(req)
    # data = resp.read()
    # print data