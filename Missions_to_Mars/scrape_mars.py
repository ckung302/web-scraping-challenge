from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    
    # Initializing browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # url being scraped - NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    # scraping title and paragraph
    news = soup.find('div', class_='list_text')
    news_title = soup.find('div', class_='content_title').text
    news_par = soup.find('div', class_='article_teaser_body').text

    # url being scraped - JPL Mars Space Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    # scraping image url
    base_url = 'https://spaceimages-mars.com/'
    image_url = soup.find('div', class_ = 'floating_text_area').a['href']
    featured_image_url = base_url + image_url

    # url being scraped - Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)[1]

    # scraping table data and converting to html string
    table_html = table.to_html(index=False)
    table_html = table_html.replace('\n', '')

    # url being scraped - Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # getting extension urls to each section
    base_url = 'https://marshemispheres.com/'
    extensions = [base_url + item.find(class_='description').a['href'] for item in soup.find_all('div', class_='item')]

    # scraping title and image url
    image_urls = []

    for url in extensions:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        title = soup.find('div', class_ = 'cover').find('h2', class_ = 'title').text.replace(" Enhanced", "")
        img_url = base_url + soup.find('img', class_ = 'thumb')['src']
        
        image_urls.append({'title': title, 'img_url': img_url})


    browser.quit()

    mars = {
        "news_title": news_title,
        "news_par": news_par,
        "featured_image_url": featured_image_url,
        "table_html": table_html,
        "hemisphere_image_urls": image_urls
    }

    return mars