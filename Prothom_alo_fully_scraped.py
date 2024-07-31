def get_data(number):
    print("Running Prothom_alo_fully_scraped")
    ##Necessary imports
    from selenium import webdriver
    from selenium.webdriver import chrome
    from selenium.webdriver import ChromeOptions
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    ## Finding Elements by XPATH
    from selenium.webdriver.common.by import By

    driver.get("https://en.prothomalo.com/search?q=road%20accident%20dhaka",)

    import time
    news_list=[]
    news_link=[]
    l=0
    for i in range(number):
        if i<15:
            
            txt=driver.find_element('xpath',f'/html/body/div/div[6]/div/div/div[1]/div[3]/div[{i+1}]/div/div/div[2]/div/h3/a')
            news_list.append(txt.text)
            news_link.append(txt.get_attribute("href"))
        else:
            if (i-15)%10==0:
                time.sleep(5)
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script(f"window.scrollTo(0, {last_height-1200})")
                try:
                    
                    driver.find_element('xpath',f'/html/body/div/div[6]/div/div/div[1]/div[3]/div[{i+1}]/span').click()
                except:
                    l=1
                if l==1:
                    time.sleep(5)
                    try:
                        driver.find_element('xpath',f'/html/body/div/div[6]/div/div/div[1]/div[3]/div[{i+1}]').click()
                    except:
                        time.sleep(5)
                        driver.find_element('xpath',f'/html/body/div/div[6]/div/div/div[1]/div[3]/div[{i+1}]').click()
                    l=0
                time.sleep(5)
            txt=driver.find_element('xpath',f'/html/body/div/div[6]/div/div/div[1]/div[3]/div[{i+1}]/div/div/div[2]/div/h3/a')
            news_list.append(txt.text)
            news_link.append(txt.get_attribute("href"))   

    ###### Scraping Publish Date and Description ######

    publish_date=[]
    text=[]
    for i in range (len(news_link)):
        driver.get(news_link[i])
        try:
            publish_date.append(driver.find_element('xpath','/html/body/div/div[6]/div/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/time/span').text)
            tmp=""
            elements = driver.find_elements(By.TAG_NAME, 'p')
            for e in elements:
                tmp=tmp+e.text
            text.append(tmp)
        except:
            publish_date.append("Not available")
            text.append("Not Available")
        time.sleep(3)

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
    return df2
    #df3.to_csv('Prothom_Alo_Description.txt',  index=False)
