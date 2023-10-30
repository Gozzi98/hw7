from pathlib import Path
import requests
import bs4
import argparse
import json



class TrendingStories:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.date = None
        self.author = None
        self.blurb = None

    def get_details(self):
        soup = get_html_trending_stories(self.url)

        title = soup.find("h1", {'class': "article-title", 'id': 'articleTitle'})
        if title:
            self.title = title.text

        date = soup.find("span", {'class': "published-date__since"})
        if date:
            self.date = date.text

        author = soup.find("span", {'class': "published-by__author"})
        if author:
            author_text = author.find('a').text if author.find('a') else author.text
            self.author = author_text

        blurb = soup.find("p", {'class': "article-subtitle"})
        if blurb:
            self.blurb = blurb.text

        return self.title, self.date, self.author, self.blurb

def get_html_trending_stories(url):
    """
    Get the HTML for the given URL. If the HTML has already been downloaded, it will be loaded from the file.

    """
    # Modify the URL to create a valid file name
    filename = url.replace('/', '_')
    fpath = Path(f'{filename}.html')       
   
    if not fpath.exists():  
        # Add a user agent to avoid being blocked by the server
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
        # Download the HTML
        data = requests.get(url, headers=headers)
        # Save it to a file
        text = data.content.decode()
        # Parse the HTML
        soup = bs4.BeautifulSoup(text, 'html.parser')
       # Save the HTML to a file
        with open(fpath, "w") as f:
            f.write(data.text) 
        return soup
    else:
        # Load the HTML from a file
        with open(fpath) as f:
            return bs4.BeautifulSoup(f, 'html.parser')

def main():
   
    parser = argparse.ArgumentParser(description='Collect trending stories from the Montreal Gazette')
    parser.add_argument("-o","--output_json_file",required=True, help="The json output file to write the data to.")
    args = parser.parse_args()
    url = 'https://montrealgazette.com/category/news/'
    soup = get_html_trending_stories(url)
    # Get the list of trending stories
    trends = soup.find("ol", {'class': "list-widget__content list-unstyled"}).contents
    
    stories = []
    # Get the details for each story
    for link in trends:
        # Get the URL for the story
        json_attr = link.next.attrs
        trend_json = json.loads(json_attr['data-evt-val'])
        url_story = trend_json['target_url']

        story = TrendingStories(url_story)
        story.get_details()
        stories.append({
            "title": story.title,
            "date": story.date,
            "author": story.author,
            "blurb": story.blurb
        }

        )

    with open(args.output_json_file, 'w') as f:
        json.dump(stories, f, indent=4)   

    return stories


if __name__ == '__main__':
    main()
   