import datetime
import requests
from flask import Flask, render_template
from flask import request
from urllib.parse import urlparse
import aiohttp
import asyncio
import copy

app = Flask(__name__)

import json
import datetime
from flask import jsonify
    
from urllib.parse import urlparse

def get_domain(url):
    try:
        data = urlparse(url)
        if data.netloc.startswith('www.'):
            return data.netloc.replace('www.','')
        else:
            return data.netloc
    except:
        None

def get_links(url):
    krakenurl = 'https://us-central1-kraken-v1.cloudfunctions.net/krakenScrapeWebpage'
    payload={}
    emptyValue = []
    payload['url'] = url
    r = requests.post(url=krakenurl, json=payload)

    links = json.loads(r.content)
    for link in links:
        print(link)
        a=1
    return links



async def fetch(url, s):
    payload={}
    emptyValue = []
    payload['url'] = url
    krakenurl = 'https://us-central1-kraken-v1.cloudfunctions.net/krakenScrapeWebpage'
    
        #async with aiohttp.ClientSession() as s: 
    response = await s.post(krakenurl, json=payload)
    print(await response.json(content_type=None))
    return await response.json(content_type=None)



async def cycle(urls):
    s = aiohttp.ClientSession() 
    return await asyncio.gather(*[fetch(url, s) for url in urls])






@app.route('/scrape/')
def scrape():
    website = request.args.get('website')
    import time

    pages_scraped = 0

    url = website

    if url is None:
        url = 'https://www.synoptek.com'

    original_url = url

    scrapped = []
    to_scrape = []

    to_scrape.append(url)

    while len(to_scrape):
        #urls = get_links(to_scrape[0])
        scrape_run=[]
        scrape_run=to_scrape.copy()
        to_scrape2=[]
        results = asyncio.run(cycle(scrape_run))
        urls=[]
        for links in results:
            for link in links:
                urls.append(link)

        pages_scraped += len(to_scrape)
        scrapped = scrapped + scrape_run


        for url in urls:
            if get_domain(url) == get_domain(original_url):
                if url not in to_scrape2:
                    if url not in scrapped:
                        to_scrape2.append(url)
        to_scrape = to_scrape2.copy()
        print(len(scrapped))
        print(len(to_scrape))
        print(pages_scraped)
    return 'Done'


@app.route('/test/')
def test():
    username = request.args.get('username')
    password = request.args.get('password')
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    times_all = [1,3,4,5]

    return render_template('test.html', times=times_all, username=username, password=password)





@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)