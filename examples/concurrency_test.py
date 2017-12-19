# -*- coding: utf-8 -*-
# from http://elliothallmark.com/2016/12/23/requests-with-concurrent-futures-in-python-2-7/

# import requests
# from concurrent.futures import ThreadPoolExecutor, wait, as_completed
# from time import time
# urls = ['google.com','cnn.com','reddit.com','imgur.com','yahoo.com']
# urls = ["http://"+url for url in urls]
# # Time requests running synchronously
# then = time()
# sync_results = map(requests.get, urls)
# print("Synchronous done in %s" % (time() - then))
# # Time requests running in threads
# then = time()
# pool = ThreadPoolExecutor(len(urls))  # for many urls, this should probably be capped at some value.
#
# futures = [pool.submit(requests.get,url) for url in urls]
# results = [r.result() for r in as_completed(futures)]
# print("Threadpool done in %s" % (time() - then))


import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://dstcontrols.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
