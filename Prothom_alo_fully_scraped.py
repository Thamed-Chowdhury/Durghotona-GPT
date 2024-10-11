def get_data(number):
    print("Running Prothom_alo_fully_scraped")
    ##Necessary imports
    from deep_translator import GoogleTranslator
    from selenium import webdriver
    from selenium.webdriver import chrome
    from selenium.webdriver import ChromeOptions
    from datetime import datetime, timedelta
    import re
    #PROXY = "45.251.231.113:5678"
    options = ChromeOptions()
    #options.add_argument('--proxy-server=%s' % PROXY)
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    ## Finding Elements by XPATH
    from selenium.webdriver.common.by import By
    import time, math
    driver.get("https://www.prothomalo.com/topic/%E0%A6%B8%E0%A7%9C%E0%A6%95-%E0%A6%A6%E0%A7%81%E0%A6%B0%E0%A7%8D%E0%A6%98%E0%A6%9F%E0%A6%A8%E0%A6%BE")
    time.sleep(15)
    news_list=[]
    news_link=[]
    publish_date=[]
    if number<=15:
        txt=driver.find_elements(By.CLASS_NAME, "title-link")
        date=driver.find_elements(By.TAG_NAME, "time")
        for i in range(number):
            news_list.append(txt[i].text)
            news_link.append(txt[i].get_attribute("href"))
            publish_date.append(date[i].text)
        
    else:
        clck=int((number-25)/15 + 2)
        for i in range(clck):
            print(i)
            time.sleep(10)
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {last_height-1050})")
            button=driver.find_elements(By.CLASS_NAME, "tNj8k")
            button[0].click()
        time.sleep(5)
        txt=driver.find_elements(By.CLASS_NAME, "title-link")
        date=driver.find_elements(By.TAG_NAME, "time")
        for i in range(number):
            news_list.append(txt[i].text)
            news_link.append(txt[i].get_attribute("href"))
            publish_date.append(date[i].text)

    ###### Scraping Description modified for translation######
    from deep_translator import GoogleTranslator
    from goose3 import Goose
    from datetime import datetime
    g = Goose()
    description=[]
    News_title=[]
    publish_date=[]
    for i in range(len(news_link)):
        print(i)
        article = g.extract(url=news_link[i])
        ### Only for Prothom Alo ###
        # Access the articleBody field
        data = article.schema
        article_body = data.get('articleBody')
        print("Para length", len(article_body))
        if(len(article_body)>=2200):
            article_body=article_body[0:2200]
        bangla_title=article.title
        english_title = GoogleTranslator(source='auto', target='en').translate(text=bangla_title)
        News_title.append(english_title)
        text = GoogleTranslator(source='auto', target='en').translate(text=article_body)
        description.append(text)
        publish_date.append(article.publish_date)
    # Convert the dates to "day-month-year" format
    formatted_dates = [datetime.fromisoformat(date).strftime('%d-%m-%Y') for date in publish_date]

    #### Converting the list to a pandas dataframe by converting the list to a dictionary  ###
    dict={'News Title':News_title,'News Link':news_link,'Publish Date':formatted_dates, 'Description':description}
    import pandas as pd
    df=pd.DataFrame(dict)
    return df