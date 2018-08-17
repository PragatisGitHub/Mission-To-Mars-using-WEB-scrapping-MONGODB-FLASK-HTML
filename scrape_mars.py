from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Initialize browser
    browser = init_browser()
    listings = {}

    ### NASA Mars News

    # Visit the Mars Nasa site for news
    url = 'https://mars.nasa.gov/news/'
    
    # Using url attribute to access the visited page’s url
    browser.visit(url)

    # Using the html attribute to get the html content of the visited page
    html = browser.html
    
    # Quitting the browser 
    browser.quit()

    MarsData = BeautifulSoup(html, "html.parser")

    Result = MarsData.select_one('ul.item_list li.slide')

    news_title = Result.find('div',class_="content_title").text

    news_p = Result.find('div',class_="article_teaser_body").text

    NASA_Mars_News = {'News_Title':news_title, 'News_Para': news_p }
    
    return(NASA_Mars_News)