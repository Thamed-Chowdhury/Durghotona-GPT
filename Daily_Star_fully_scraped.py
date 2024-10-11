def get_data(number):    
    print("Running Daily_Star_Fully_Scraped")
    ##Necessary imports
    from selenium import webdriver
    from selenium.webdriver import chrome
    from selenium.webdriver import ChromeOptions
    options = ChromeOptions()
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    # Set a timeout for the page to load (in seconds)
    driver.set_page_load_timeout(10)  # Limit page loading time to 10 seconds

    ## Finding Elements by XPATH
    from selenium.webdriver.common.by import By
    driver.get("https://www.thedailystar.net/news/bangladesh/accidents-fires")
    ### Extracting first 8 news seperately
    import time
    news_list=[]
    news_link=[]
    for i in range(2,10):
        txt=driver.find_element('xpath',f'/html/body/div[3]/div/div/div/div[2]/main/div/div[2]/div/div[1]/div/div/div/div[{i}]/div/div/h3/a')
        news_list.append(txt.text)
        news_link.append(txt.get_attribute("href")) 
    # Rest of the News_title and news link extraction
    number2=number-8
    import time
    if number2>0:
        for i in range(number2):
            #time.sleep(5)
            if (i+1)!=0 and (i+1)%10==0:
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script(f"window.scrollTo(0, {last_height-950})")
                driver.find_element('xpath',f'/html/body/div[3]/div/div/div/div[2]/main/div/div[2]/div/div[3]/div/div/div[1]/div/div[2]/ul/li/a').click()
                time.sleep(10)
            txt=driver.find_element('xpath',f'/html/body/div[3]/div/div/div/div[2]/main/div/div[2]/div/div[3]/div/div/div[1]/div/div[1]/div[{i+1}]/div[2]/h3/a')
            news_list.append(txt.text)
            news_link.append(txt.get_attribute("href")) 
    # Goose3 extraction
    for i in range(len(news_link)):
        from deep_translator import GoogleTranslator
        from goose3 import Goose
        from datetime import datetime
        g = Goose()
        description=[]
        News_title=[]
        publish_date=[]
        for i in range(len(news_link)):
            article = g.extract(url=news_link[i])
            News_title.append(article.title)
            description.append(article.cleaned_text)
            publish_date.append(article.publish_date)
    # Convert the dates to "day-month-year" format
    formatted_dates = [datetime.fromisoformat(date).strftime('%d-%m-%Y') for date in publish_date]

    #### Converting the list to a pandas dataframe by converting the list to a dictionary  ###
    dict={'News Title':News_title,'News Link':news_link,'Publish Date':formatted_dates, 'Description':description}
    import pandas as pd
    df=pd.DataFrame(dict)
    return df
            