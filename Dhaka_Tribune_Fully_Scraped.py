def get_data(number):
    ##Necessary imports
    from selenium import webdriver
    from selenium.webdriver import chrome
    from selenium.webdriver import ChromeOptions
    import math
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    ## Finding Elements by XPATH
    from selenium.webdriver.common.by import By


    driver.get("https://www.dhakatribune.com/topic/road-accident")

    #### Scraping News Title and News Link ####
    import time
    news_list=[]
    news_link=[]
    publish_date=[]
    row_counter=0
    news_counter=0
    for i in range(number):
        if i==0:
            row_counter=1
        else:
            row_counter=math.ceil(i/4)
        news_counter=i%4+1
        #time.sleep(5)
        if (i+1)!=0 and (i+1)%20==0:
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {last_height})")
            driver.find_element('xpath',f'/html/body/div[3]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[2]/button').click()
            time.sleep(10)
        txt=driver.find_element('xpath',f'/html/body/div[3]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[1]/div[{row_counter}]/div[{news_counter}]/div/div[2]/div/div/div/h2/a')
        #publish_date.append(driver.find_element('xpath',f'/html/body/div[3]/div/div/div/div[2]/main/div/div[2]/div/div[5]/div/div/div[1]/div/div[1]/div[{i+1}]/div[1]').text)
        news_list.append(txt.text)
        news_link.append(txt.get_attribute("href")) 
    
    ###### Scraping Publish Date ######
    publish_date=[]
    for i in range (len(news_link)):
        driver.get(news_link[i])
        time.sleep(6)
        driver.execute_script("window.stop();")
        try:
            publish_date.append(driver.find_element('xpath','/html/body/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div[1]/div/div[2]/span[1]').text)
        except:
            publish_date.append("Not available")

    #### Converting the list to a pandas dataframe by converting the list to a dictionary  ###
    dict={'News Title':news_list,'News Link':news_link,'Publish Date':publish_date}
    import pandas as pd
    df=pd.DataFrame(dict)


    ############################################ Description Extraction ###################################################

    from newspaper import Article
    text=[]
    for i in range(len(df)):
        url = df['News Link'][i]
        article = Article(url)
        article.download()
        article.parse()
        
        text.append(article.text)


    df2=df.assign(Description=text)
    for p in range(len(df2)):
        if df2['Publish Date'][p]=="Not available":
            df2.drop([p],inplace=True)

    df2.reset_index(drop=True,inplace=True)
    df2["Date + Desc"]=df2['Publish Date'] + ".     News Description:"+ df2['Description']


   
    return df2
    
    #df3.to_csv('Dhaka_Tribune_Description.txt',  index=False)