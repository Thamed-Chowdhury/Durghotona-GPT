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
    options.add_argument("--headless=new")
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
    text=[]
    for i in range (len(news_link)):
        driver.get(news_link[i])
        try:
            tmp=""
            elements = driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(elements)):
                if i>2 and len(tmp+elements[i].text) < 2000:
                    tmp=tmp+elements[i].text
                    
            text.append(tmp)
        except:
            text.append("Not Available")
        time.sleep(5)
    ## Translation 
    for i in range(len(news_list)):
        news_list[i] = GoogleTranslator(source='auto', target='en').translate(text=news_list[i])
        text[i] = GoogleTranslator(source='auto', target='en').translate(text=text[i])
        publish_date[i] = GoogleTranslator(source='auto', target='en').translate(text=publish_date[i])

    #### Converting the list to a pandas dataframe by converting the list to a dictionary  ###
    dict={'News Title':news_list,'News Link':news_link,'Publish Date':publish_date, 'Description':text}
    import pandas as pd
    df=pd.DataFrame(dict)
    df2=df.copy()


    for p in range(len(df2)):
        if df2['Publish Date'][p]=="Not available":
            df2.drop([p],inplace=True)
    #df2.reset_index()
    df2["Date + Desc"]=df2["Publish Date"] + df2["Description"]
    df2.reset_index(drop=True,inplace=True)
    # Function to convert relative time to date and format as day-month-year
    def convert_relative_time_to_date(time_str):
        if 'hours ago' in time_str:
            hours = int(re.search(r'(\d+)', time_str).group(1))
            return (datetime.now() - timedelta(hours=hours)).strftime('%d-%m-%Y')
        elif 'days ago' in time_str:
            days = int(re.search(r'(\d+)', time_str).group(1))
            return (datetime.now() - timedelta(days=days)).strftime('%d-%m-%Y')
        else:
            # If it's already a date string, return it in day-month-year format
            return pd.to_datetime(time_str).strftime('%d-%m-%Y')

    # Apply the function to the DataFrame
    df2['Publish Date'] = df2['Publish Date'].apply(convert_relative_time_to_date)

    return df2
    #df3.to_csv('Prothom_Alo_Description.txt',  index=False)
