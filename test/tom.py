import time
import requests

from tomorrow import threads

URLS = [
    "http://www.baidu.com"
]


@threads(5)
def download(url):
    return requests.get(url)


if __name__ == "__main__":
    start = time.time()
    responses = [download(url) for url in URLS]
    html = [response.text for response in responses]
    print len(responses)
    end = time.time()
    print "Time: %f seconds" % (end - start)