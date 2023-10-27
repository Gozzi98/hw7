from pathlib import Path
import requests
import bs4
import argparse

"""
well be using web scraping to collect the 5 trending stories from the Montreal Gazette. 
Our objective is to collect the title, publication date, author, and opening “blurb

”"""
def get_5_trending_stories():
    fpath = Path('montreal_gazette_trending.html')
    
    if not fpath.exists():  
        url = 'https://montrealgazette.com/category/news/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
        data = requests.get(url, headers=headers)
        text = data.content.decode()
        soup = bs4.BeautifulSoup(text)
        
        with open(fpath, "w") as f:
            f.write(data.text) 
        return text, soup
    
    with open(fpath, "r") as f:
        return f.read()   
def main():
    parser = argparse.ArgumentParser()
    argparse.ArgumentParser(description='Collect trending stories from the Montreal Gazette')
    args = parser.parse_args()

    top_5 = get_5_trending_stories()
    soup = bs4.BeautifulSoup(top_5, 'html.parser')

    table = soup.find("li", {'class': "article-card__content first"})
    print("hi")
    for link in soup.find_all('a'):
        print(link.get('href'))
    
    print(top_5)

if __name__ == '__main__':
    main()