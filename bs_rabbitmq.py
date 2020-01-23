from queue import Queue
import requests
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import simplejson

base_url = 'https://news.cnblogs.com'
newspath = "/n/page/"
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}

from messagequeue import Producer, Consumer

# urls = Queue()
# htmls = Queue()
# outputs = Queue()
event = threading.Event()


def gen_urls(start, end, step=1):
    p = Producer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'urls')
    for i in range(start, end + 1, step):
        url = '{}{}{}'.format(base_url, newspath, i)
        p.SendMsg(url)

def crawler():
    try:
        c = Consumer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'urls')
        p = Producer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'htmls')
        while not event.wait(1):
            url = c.ReceiveMsg()
            if url:
                with requests.request('GET', url, headers=headers) as response:
                    text = response.text
                    # htmls.put(text)
                    p.SendMsg(text)
            else:
                pass
    except Exception as e:
        print('e:', "1111111", e)


def parse():
    try:
        c = Consumer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'htmls')
        p = Producer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'outputs')
        while not event.is_set():
            # html = htmls.get(True,1)
            html = c.ReceiveMsg()
            if html:
                soup = BeautifulSoup(html, 'lxml')
                news = soup.select('h2.news_entry a')
                # print(news)
                for new in news:
                    href = new.get('href', None)
                    if href:
                        # print(href)
                        url = base_url + href
                        title = new.text
                        # outputs.put((url, title))
                        p.SendMsg(simplejson.dumps({'url': url, 'title': title}))
            else:
                event.wait(1)
    except Exception as e:
        print(e)


def persist(path):
    c = Consumer('192.168.126.129', 5672, 'test1', 'baichen111', '12345', 'news', 'outputs')
    with open(path, 'a+', encoding='utf-8') as f:
        while not event.is_set():
            try:
                # text = '{}\x01{}\n'.format(*outputs.get(True,1))
                data = c.ReceiveMsg()
                if data:
                    data = simplejson.loads(data)
                    text = '{}\: {}\n'.format(data['url'], data['title'])
                    print(text)
                    f.write(text)
                    f.flush()
                else:
                    event.wait(1)
            except:
                raise


executor = ThreadPoolExecutor(10)  # 10 threads in pool
executor.submit(gen_urls, 1, 50)

for _ in range(4):  # put 4 threads into pool
    executor.submit(crawler)
for _ in range(5):  # put 5 threads into pool
    executor.submit(parse)

executor.submit(persist, 'news.html')  # put 1 thread to pool

#
# session = requests.session()
# with session :
#     with session.get(url,headers=headers) as response:
#         #爬取
#         text = response.text
#
#         print(text)
#
#         # with open('sina.html','w',encoding='utf-8') as f:
#         #     f.write(text)
