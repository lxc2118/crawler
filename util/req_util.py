# coding=utf-8
# __author__ = 'zhiwei'


def get_url_param(dist):
    temp_list = []
    for k, v in dist:
        temp_list.append(str(k) + "=" + str(v))
    if temp_list:
        return "?" + "&".join(temp_list)
    return ""