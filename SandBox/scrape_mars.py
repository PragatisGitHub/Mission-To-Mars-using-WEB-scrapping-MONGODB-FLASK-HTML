# Import Dependencies
import pandas as pd # Import pandas to read the html page
import time

from splinter import Browser
from bs4 import BeautifulSoup

import tweepy
from config import (consumer_key, consumer_secret, 
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Function to initialize the browser for chrome
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

Mars_Data = {}

def scrape():
    
### NASA Mars News
    
    # Initialize browser
    browser = init_browser()
    
    NASA_Mars_News = {}

    # Visit the Mars Nasa site for news
    url = 'https://mars.nasa.gov/news/'
    
    # Using url attribute to access the visited page’s url
    browser.visit(url)
    time.sleep(2)

    # Using the html attribute to get the html content of the visited page
    html = browser.html
    
    # Create a soup object to find the latest news from the URL
    MarsNewsData = BeautifulSoup(html, "html.parser")

    Result = MarsNewsData.select_one('ul.item_list li.slide')

    news_url_link = Result.find('div',class_="image_and_description_container").a['href']
    
    news_published_date = Result.find('div',class_="list_date").text

    news_title = Result.find('div',class_="content_title").text

    news_p = Result.find('div',class_="article_teaser_body").text

    Mars_Data['News_Title'] = news_title
    Mars_Data['News_Para'] = news_p
    Mars_Data['News_Published_Date'] = news_published_date
    Mars_Data['News_url_link'] = "https://mars.nasa.gov" + news_url_link

### JPL Mars Space Images - Featured Image

    # Visit jpl NASA site for the featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Using url attribute to access the visited page’s url
    browser.visit(url)
    time.sleep(2)
    
    # Using the html attribute to get the html content of the visited page
    html = browser.html

    # Create a soup object to find the featured image from the URL
    MarsImageData = BeautifulSoup(html,"html.parser")

    Mars_Img_Art = MarsImageData.find('div',class_='carousel_items').find("article",class_="carousel_item").get("style")
    image = Mars_Img_Art.split("('",2)[1].split("')",2)[0]
    Mars_Img_Title = MarsImageData.find('div',class_='carousel_items').find("article",class_="carousel_item").get("alt")


    featured_image_url = 'https://www.jpl.nasa.gov'+ image
    
    Mars_Data['Featured_Image_Url'] = featured_image_url
    Mars_Data['Featured_Image_Title'] = Mars_Img_Title
    
    
### Mars Weather

    # Target User Account
    target_user = "@MarsWxReport"

    # Get all tweets from home feed
    public_tweets = api.user_timeline(target_user)

    mars_weather = ""
    flag = False

    for tweet in public_tweets:
        if flag == True:
            mars_weather = tweet["text"]
            flag = False
            break
        else:  
            if 'Sol' in tweet["text"]:
                flag = True
    
    Mars_Data['Weather'] = mars_weather
    
### Mars Facts
    
    # Visit space facts site for the Mars facts
    url = 'http://space-facts.com/mars/'

    # Using url attribute to access the visited page’s url
    browser.visit(url)
    time.sleep(2)
    
    # Using the html attribute to get the html content of the visited page
    html = browser.html
   
    # Create a soup object to find the Mars facts from the URL
    MarsFactsData = BeautifulSoup(html,"html.parser")

    MarsFactsData.find_all('table')

    Marstab = MarsFactsData.find_all('table')

    df = pd.read_html(str(Marstab))

    df=df[0].set_index([0])

    df=df.rename(columns={1:"Values"})

    marsfactshtml = df.to_html()

    Mars_Data['Facts_Table'] = marsfactshtml
    
### Mars Hemispheres
    
    # Visit the US govt.'s astrology site for the Mars hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Using url attribute to access the visited page’s url
    browser.visit(url)
    time.sleep(2)
    
    # Using the html attribute to get the html content of the visited page
    html = browser.html

    # Quitting the browser 
    browser.quit()

    # Create a soup object to find the Mars hemispheres from the URL
    MarsHemisphereImage = BeautifulSoup(html, "html.parser")

    Img4 = MarsHemisphereImage.find('div', class_='collapsible').find_all('a', class_='product-item')

    url = "https://astrogeology.usgs.gov"

    index = 0
    mars_hemispheres_list = []
    
    for img in Img4:
        if index%2!=0:
            title = img.find('h3').text

            url1 = url+img.get('href')

            #Initialize the browser    
            browser = init_browser()

            # Using url attribute to access the visited page’s url    
            browser.visit(url1)
            time.sleep(2)
            
            # Using the html attribute to get the html content of the visited page
            html = browser.html

            # Quitting the browser 
            browser.quit()

             # Create a soup object to find the enlarged image of the Mars hemispheres from the URL
            MarsHemisphereImages = BeautifulSoup(html, "html.parser")

            MarshemisImage = MarsHemisphereImages.find('img', class_='wide-image')

            link = MarshemisImage.get('src')

            Image_url = url+link

            mars_hemispheres_list.append({'title':title,'img_url':Image_url})

        index=index+1
        
    Mars_Data['Mars_Hemispheres'] = mars_hemispheres_list
                                                            
    return(Mars_Data)                                                    