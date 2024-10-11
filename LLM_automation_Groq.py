def create_data(description):
    print("Running LLM Automation Groq")
    from langchain_core.prompts import ChatPromptTemplate  ### To create a chatbot, chatprompttemplate used

    from langchain_core.output_parsers import StrOutputParser  ### Default output parser. Custom parser can also be created
    from langchain_groq import ChatGroq


    import os
    from dotenv import load_dotenv
    import pandas as pd

    load_dotenv()

    ### Set all api keys:


    os.environ["GROQ_API_KEY"]="ENTER YOUR API HERE"



    ### Create Prompt Template:
    prompt=ChatPromptTemplate.from_messages(
        {
            ("system", "You are a helpful assistant, please respond to the queries"), ### We need both system and users in prompt
            ("user","question: {question}")
        }
    )

    #### Create LLama3 70B llm:
    llm = ChatGroq(
        model="llama3-70b-8192"
    )  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `


    ### Create an output parser:
    output_parser=StrOutputParser()

    #### Creating chain: The concept is- output of action before | symbol will be passed as input in action after the symbol.
    #### Here we have created three actions: The prompt, llm and output parser:
    chain=prompt|llm|output_parser

    df = description
    df = df.fillna(0)
    dj=[]
    for i in range(len(df)):
        dj.append(chain.invoke({"question" : df['Description'][i]+" Is the news about road accident? If no, then reply 'General'. Else if the news is about road accident then check if the news is referring to a specific accident incident or accident in general? Answer only in a word: Either specific or general."}))
        
    df2=df.copy()
    df2['Report Type']=dj
    df2.to_csv('Report Categoriztion.csv',index=False)
    def drp(p):
        df2.drop([p],inplace=True)
    
    ### Removing the general accident types:
    for p in range(len(df)):
        if "General" in df2['Report Type'][p]:
            drp(p)
            
    ### Reseting index of df3:
    df2.reset_index(drop=True,inplace=True)

    ### Now finding column values using llm:
    ### A function to invoke the llm. For some reason phi3 doesn't give accurate result sometimes if used directly in dj.append()
    def res(i):
        response=chain.invoke({"question" : f"""I will give you two strings. 1st string will contain a publish date of a news and the 2nd string will contain the accident news itself. 
                            If the 2nd string contains more than one accident incidents, only consider the 1st incident. Based on these two strings, you have to answer the following questions. Remember your answer must contain ONLY THE ANSWERS WITHOUT ANY EXTRA WORDS OR SENTENCES:
                            what is the date (Day-Month-Year numerical format) of accident occurrence? ;
                            Time of Accident occured; How many people were killed in the accident?; 
                            How many people were injured in the accident?;
                            Location of the accident; 
                            Type of road where accident occured; 
                            Was there any pedestrian involved?;  
                            Do not include any extra words or sentences except the answers seperated by semicolons only. Your reply cannot contain sentences such as - 'Here are the answers to the questions'
                            string 1 = {df2['Publish Date'][i]}
                            string 2 = {df2['Description'][i]}""" })
        return response
    #### dj2 list contains all column values seperated by comma:
    dj2=[]

    for i in range(len(df2)):
        dj2.append(res(i))

### A function to invoke the llm. For some reason phi3 doesn't give accurate result sometimes if used directly in dj.append()
    def res2(i):
        response=chain.invoke({"question" : df2['Description'][i]+" Only name the type of vehicles involved in the accident. If multiple vehicles are involved, seperate them by hyphens(-). Example answers: Bus, Truck-Bus etc. If no vehicles are mentioned, your answer will be: Not Available. Your answer should only contain the vehicle name, do not include any extra sentences"})
        return response
    #### dj2 list contains all column values seperated by comma:
    vehicles=[]

    for i in range(len(df2)):
        vehicles.append(res2(i))


    ### Splitting dj2 string based on comma position:
    Date=[]
    Time=[]
    Killed=[]
    Injured=[]
    Location=[]
    Road_Characteristic=[]
    Pedestrian_Involved=[]
    #Vehicles_involved=[]

    for i in range(len(dj2)):
        words = dj2[i].split(";")  # Splitting at the semicolon delimiter
        #print(f"Date: {words[0]}")
        Date.append(words[0])
            
        #print(f"Time: {words[1]}")
        Time.append(words[1])
            
        #print(f"Casualities: {words[2]}")
        Killed.append(words[2])
        Injured.append(words[3])
        Location.append(words[4])
        Road_Characteristic.append(words[5])
        Pedestrian_Involved.append(words[6])
        #Vehicles_involved.append(words[7])

    #### Probable type of final dataframe:
    df2["Accident Date"]=Date
    df2["Time"]=Time
    df2["Killed"]=Killed
    df2["Injured"]=Injured
    df2["Location"]=Location
    df2["Road_Characteristic"]=Road_Characteristic
    df2["Pedestrian_Involved"]=Pedestrian_Involved
    df2["Vehicles_involved"]=vehicles
    df3=df2.drop(columns=['Description','Report Type'])
    df3.to_csv('Info Extract.csv',index = False)
    return df3
    


