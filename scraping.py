# D-2; Step 2

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    hemisphere_image_urls = mars_hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")

# D-2; Step 3
def mars_hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    hemisphere_image_urls = []
    results = img_soup.find("div", class_ = 'collapsible results')
    mars_img = results.find_all('div', class_='item')
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemispheres = {}
        browser.find_by_css('a.product-item img')[i].click()
        mars_title = browser.find_by_css("h2.title").text
        sample = browser.links.find_by_text('Sample').first
        img_url_rel = sample['href']
        hemispheres["img_url"] = img_url_rel
        hemispheres["title"] = mars_title
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())