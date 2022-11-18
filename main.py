import http.client
import json
import urllib.request
from threading import Thread
from urllib import error
import time
import requests
import urllib3.exceptions

DOWNLOAD_PATH = r'dump/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def threaded_f(first, last, start, finish):
    isvalid = True
    for i in range(int(first), int(last)):
        if i > finish:
            break
        print(i)
        try:
            j = json.loads(requests.get(url + str(i), HEADERS).content)
        except urllib.error.HTTPError as err:
            print('HTTPError', err)
            continue
        except urllib.error.URLError:
            print('URLError')
            continue
        except http.client.RemoteDisconnected:
            print('DisconnError')
            continue
        except json.decoder.JSONDecodeError:
            print('JsonDecode Error')
            continue
        except requests.exceptions.ConnectionError:
            print('Connection Error')
            continue
        if 'id' in j:
            try:
                print(str(j['id']) + ', ' + j['source_url'])
            except UnicodeEncodeError as a:
                print(str(j['id']))
            with open("media_planetel" + str(start) + "_" + str(finish) + "_2.csv", "a") as file_object:
                try:
                    file_object.write(str(j['id']) + ', ' + j['source_url'] + '\n')
                except UnicodeEncodeError as a:
                    print(str(j['id']))
            isvalid = True
            while isvalid:
                try:
                    file = requests.get(j['source_url'], allow_redirects=True, timeout=2)
                    isvalid = False
                except requests.exceptions.ConnectionError as a:
                    print(a)
                    isvalid = False
                    continue
                except requests.exceptions.ReadTimeout as a:
                    print(a)
                    isvalid = False
                    continue
                except urllib3.exceptions.SSLError as a:
                    print(a)
                    isvalid = True

                name = j['source_url'].split('/')
                try:
                    open(DOWNLOAD_PATH + name[len(name) - 1].replace(' ', '_'), 'wb').write(file.content)
                except UnboundLocalError as a:
                    print(a)
                    continue

if __name__ == "__main__":
    ad = int(input("Inserire ultimo valore scaricato: "))
    thread_number = 10

    url = 'https://www.asl1sassari.it/wp-json/wp/v2/media/'
    first = 0
    last = 29441
    length = (last - first) / thread_number
    thread_list = []
    while True:
        j = json.loads(requests.get(url, HEADERS).content)
        last = j[0]['id']
        print('last:', last)
        if last != ad:
            for i in range(1, thread_number):
                thread_list.append(Thread(target=threaded_f,
                                          args=(((i - 1) * length) + ad, (i * length) + ad, first, last)))
                thread_list.pop().start()
        ad = last
        print('--- FINE SERIE ---')
        time.sleep(3600)

