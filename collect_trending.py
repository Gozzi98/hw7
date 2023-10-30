from pathlib import Path
import requests
import bs4
import argparse
import json
from urllib.parse import urlparse
"""
well be using web scraping to collect the 5 trending stories from the Montreal Gazette. 
Our objective is to collect the title, publication date, author, and opening “blurb

”"""
 

def get_html_trending_stories(url):
    
    url_parts = urlparse(url)
    hostname = url_parts.hostname
    fpath = Path(f'{hostname}.html')

    if not fpath.exists():  
        #url = 'https://montrealgazette.com/category/news/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
        data = requests.get(url, headers=headers)
        text = data.content.decode()
        soup = bs4.BeautifulSoup(text, 'html.parser')
        
        with open(fpath, "w") as f:
            f.write(data.text) 
        return soup
    else:
        with open(fpath) as f:
            return bs4.BeautifulSoup(f, 'html.parser')
def get_url_stories(url):
    
    parser = argparse.ArgumentParser()
    argparse.ArgumentParser(description='Collect trending stories from the Montreal Gazette')
    args = parser.parse_args()
    args.url = url
    
    soup = get_html_trending_stories(args.url)

    trends = soup.find("ol", {'class': "list-widget__content list-unstyled"}).contents
    
    url = []
    for link in trends:
        json_attr = link.next.attrs
        trend_json = json.loads(json_attr['data-evt-val'])
        url_story = trend_json['target_url']
        url.append(url_story)
    return url
    
class TrendingStories:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.date = None
        self.author = None
        self.blurb = None

    def get_details(self):
        soup = get_html_trending_stories(self.url)

        title_element = soup.find("h1", {'class': "article-title", 'id': 'articleTitle'})
        if title_element:
            self.title = title_element.text

        date_element = soup.find("span", {'class': "published-date__since"})
        if date_element:
            self.date = date_element.text

        author_element = soup.find("span", {'class': "published-by__author"})
        if author_element:
            author_text = author_element.find('a').text if author_element.find('a') else author_element.text
            self.author = author_text

        blurb_element = soup.find("p", {'class': "article-subtitle"})
        if blurb_element:
            self.blurb = blurb_element.text

        return self.title, self.date, self.author, self.blurb


if __name__ == '__main__':
    url = 'https://montrealgazette.com/category/news/'
    get_html_trending_stories(url)    #class treding stories object

    links = get_url_stories(url)
    for link in links:
        story = TrendingStories(link)
        story.get_details()
        print(story.title)
        print(story.date)
        print(story.author)
        print(story.blurb)
        print()

    