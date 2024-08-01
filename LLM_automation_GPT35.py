def create_data(description):
    from langchain_core.prompts import ChatPromptTemplate  ### To create a chatbot, chatprompttemplate used
    from langchain_openai import ChatOpenAI ##### For using chat openai features
    from langchain_core.output_parsers import StrOutputParser  ### Default output parser. Custom parser can also be created
    


    import os
    from dotenv import load_dotenv


    load_dotenv()

    ### Set all api keys:
    os.environ["OPENAI_API_KEY"]="ENTER YOUR API HERE"


    ### Create Prompt Template:
    prompt=ChatPromptTemplate.from_messages(
        {
            ("system", "You are a helpful assistant, please respond to the queries"), ### We need both system and users in prompt
            ("user","question: {question}")
        }
    )
    df2=description
    #### Create OpenAI llm:
    llm=ChatOpenAI(model="gpt-3.5-turbo")

    ### Create an output parser:
    output_parser=StrOutputParser()

    #### Creating chain: The concept is- output of action before | symbol will be passed as input in action after the symbol.
    #### Here we have created three actions: The prompt, llm and output parser:
    chain=prompt|llm|output_parser

    ### A function to invoke the llm. For some reason phi3 doesn't give accurate result sometimes if used directly in dj.append()
    def res(i):
        response=chain.invoke({"question" : df2['Description'][i]+" Is the news referring to a specific accident incident or accident in general? Answer only in a word: 'specific' or 'general'. No other words are allowed in your answer"})
        return response

    #### dj list contains type of report 'General' or 'Specific'
    dj=[]

    for i in range(len(df2)):
        dj.append(res(i))

    df2['Report Type']=dj

    def drp(p):
        df2.drop([p],inplace=True)
    ### Removing the general accident types:
    for p in range(len(df2)):
        if "General" in df2['Report Type'][p] or "general" in df2['Report Type'][p]:
            drp(p)
            
    ### Reseting index of df3:
    df2.reset_index(drop=True,inplace=True)


    ### Splitting dj2 string based on comma position:
    Date=[]
    Time=[]
    Killed=[]
    Injured=[]
    Location=[]
    Road_Characteristic=[]
    Pedestrian_Involved=[]
    vehicles=[]
    #Weather=[]

    for i in range(len(df2)):
        Date.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: What is the date of accident occurrence in Day-Month-Year format. Keep in mind that news publish date and accident occurrence date may be different. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Time.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: What is the time of accident occurrence in 24-hour format. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Killed.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: How many people were killed in the accident?. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Injured.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: How many people were injured in the accident?. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Location.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: What is the name of the location where accident took place?. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Road_Characteristic.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: What is the type of road where accident took place?. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        Pedestrian_Involved.append(chain.invoke({"question" : "Read the accident report carefully and provide only the answer of the question asked. Do not add any extra sentences or words except the answer: Was there any pedestrian involved in the accident?. If you cannot find or deduce the answer, simply reply Not Available" + df2['Description'][i]}))
        vehicles.append(chain.invoke({"question" : "Only name the type of vehicles involved in the accident. If multiple vehicles are involved, seperate them by hyphens(-). Example answers: Bus, Truck-Bus etc. If no vehicles are mentioned, your answer will be: Not Available. Your answer should only contain the vehicle name, do not include any extra sentences" + df2['Description'][i]}))
        
    #### Probable type of final dataframe:
    df2["Date"]=Date
    df2["Time"]=Time
    df2["Killed"]=Killed
    df2["Injured"]=Injured
    df2["Location"]=Location
    df2["Road_Characteristic"]=Road_Characteristic
    df2["Pedestrian_Involved"]=Pedestrian_Involved
    df2["Vehicles Involved"]=vehicles
    df3=df2.drop(columns=['Description','Report Type','Date + Desc'])
    return df3
