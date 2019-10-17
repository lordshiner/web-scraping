#!/usr/bin/env python
# coding: utf-8

# In[1]:


def scrape ():
    # Dependencies
    from bs4 import BeautifulSoup as bs
    import requests
    import pandas as pd
    from splinter import Browser

    # Establish Splinter connection
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Target Site to Scrape
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)

    # Set up Soup Object
    html = browser.html
    soup = bs(html, 'html.parser')
    
    
    # Grab latest article and title
    element = soup.select_one('ul.item_list li.slide' )
    divs = element.find('div' , class_='content_title')
    divs2 = element.find('div', class_='article_teaser_body')

    title1 = divs.get_text()
    link1 = divs.a.attrs['href']
    Para1 = divs2.get_text()

    #close the active Browser
    browser.quit()
    
    # Establish 2nd Splinter connection
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser2 = Browser('chrome', **executable_path, headless=False)

    # Target 2nd Site to Scrape with 2nd Soup Object
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser2.visit(url2)
    html2 = browser2.html
    soup2 = bs(html2, 'html.parser')
    
    
    # Navigate to full image (Button) with Splinter 
    button = soup2.find('a',class_='button fancybox')
    link2 = button.attrs['data-fancybox-href']
    browser2.click_link_by_partial_text('FULL IMAGE')

    #Save Full URL of Full Size Image from 2nd Site
    featured_image_url = (f'https://www.jpl.nasa.govlink2{link2}')

    #close the active Browser
    browser2.quit()

    # Establish 3rd Splinter connection
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser3 = Browser('chrome', **executable_path, headless=False)

    # Target 3rd Site to Scrape the latest Mars weather tweet from the page
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser3.visit(url3)
    html3 = browser3.html
    soup3 = bs(html3, 'html.parser')
    
    
    tweet = soup3.select_one("div.js-tweet-text-container")
    mars_weather = tweet.find('p' , class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    #mars_weather
    #close the active Browser
    browser3.quit()

    # Target 4th Site to Scrape the table with Pandas containing facts about the planet including Diameter, Mass, etc.
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)

    # Use Pandas to clean up table and convert to DataFrame without Indexes
    df = tables[0]
    df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    df.set_index('Mars-Earth Comparison', inplace=True)
    #df.head()

    # Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html()
    #html_table 
    
    ### Mars Hemispheres
    # Establish 4th Splinter connection
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser5 = Browser('chrome', **executable_path, headless=False)

    # Target 5th Site to Scrape both the image url for image, and title 
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser5.visit(url5)
    html5 = browser5.html
    soup5 = bs(html5, 'html.parser')

    base_url = 'https://astrogeology.usgs.gov'
    titles = []
    href_paths = []
    imgurls = []

    path = soup5.find_all("div", class_="description")

    for items in path:
        href = items.a.attrs['href']
        pathstring = (f'{base_url}{href}')
        header = items.h3.text
        href_paths.append(pathstring)
        titles.append(header)
        
    

    browser5.quit()    
    #print("Items Appended")
    
      # Establish 5th Splinter connection for various site itteration
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser6 = Browser('chrome', **executable_path, headless=False)

    # Itterate through various sites to obtain High Resolution Image
    for links in href_paths:
        browser6.visit(links)
        html6 = browser6.html
        soup6 = bs(html6, 'html.parser')
        
        try:
            thumb = soup6.find('div',class_='downloads')
            track = thumb.find_all("a")
            for anch in track:
                if anch.text == 'Original':
                    imgurls.append(anch.attrs['href'])
        except:
            imgurls.append("Not_Found")
            continue

    browser6.quit()
    #print("Itteration Complete")  
    
    #Use a Python dictionary to store the data using the keys `img_url` and `title`.
    hemisphere_image_urls = []
    tracker = -1
    for M in titles:
        tracker = tracker +1
        p = {"title": titles[tracker],"img_url":imgurls[tracker]}
        hemisphere_image_urls.append(p)
        
        alldict = {"Ltitle": title1,
                   "Ltext": Para1,
                   "Fimage": featured_image_url,
                   "weather": mars_weather,
                   "Facts" : html_table,
                   "Hemi" : hemisphere_image_urls}
    return(alldict);
  
  
if __name__ == "__main__" :
    scrape()   

