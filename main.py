import datetime

from flask import Flask, render_template
from flask import request


app = Flask(__name__)

import json
import datetime
from flask import jsonify
    
from urllib.parse import urlparse



def get_links(webpage):
    krakenurl = 'https://us-central1-kraken-v1.cloudfunctions.net/krakenScrapeWebpage'
    payload={}
    emptyValue = []
    payload['url'] = url
    r = requests(webpage, json=payload)
    links = json.loads(r)
    return links


@app.route('/scrape/')
def scrape():
    website = request.args.get('website')
    import time

    url = website

    if url is None:
        url = 'https://www.synoptek.com'

    scrapped = []
    to_scrape = []

    to_scrape.append(url)

    while len(to_scrape):
        urls = get_links(to_scrape[0])
        for url in urls:
            if url not in to_scrape:
                if url not in scrapped:
                    to_scrape.append(url)
        scrapped.append(to_scrape[0])
        to_scrape.pop(0)



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