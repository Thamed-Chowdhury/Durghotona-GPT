def create_data(description):
    from langchain_core.prompts import ChatPromptTemplate  ### To create a chatbot, chatprompttemplate used

    from langchain_core.output_parsers import StrOutputParser  ### Default output parser. Custom parser can also be created
    from langchain_groq import ChatGroq


    import os
    from dotenv import load_dotenv
    import pandas as pd

    load_dotenv()

    ### Set all api keys:

    #os.environ["LANGCHAIN_TRACING_V2"]="true" ### Will automatically trace our codes using Langsmith
    os.environ["GROQ_API_KEY"]="ENTER YOUR API HERE"  #### Will be used for monitoring the calls to and from llm (both free and paid)

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
        dj.append(chain.invoke({"question" : df['Date + Desc'][i]+" Is the news referring to one or many specific accident incidents or accident in general? Make sure that your answer is only in one word. If a report contains more than one accident incident, classify it as a general accident incident. The word should be either 'Specific' or 'General'. Your answer should not contain any words except 'Specific' and 'General'  "}))
        
    df2=df.copy()
    df2['Report Type']=dj
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
        response=chain.invoke({"question" : df2['Description'][i]+f"""Provide only the answers of the following question seperated by a comma only:
                            If the news was published on {df2['Publish Date'][i]}, what is the date of accident occurrence? The date must be in Day-Month-Year format. Be careful because publish date and accident occurrence date may or may not be the same. Try to deduce correct accident date,
                            Time of Accident occured, How many people were killed in the accident in numeric number?, 
                            How many people were injured in the accident in numeric number?, 
                            Location of the accident, 
                            Type of road where accident occured, 
                            Was there any pedestrian involved?,  
                            Do not include any other sentences except the answers seperated by comma only and do not include sentences such as: Here are the answers, 
                            if you cannot find or deduce a answer simply put 'Not Available' in place of it. 
                            If a report mentions more than one specific accident incidents only consider the 1st accident incident and ignore the second one""" })
        return response
    #### dj2 list contains all column values seperated by comma:
    dj2=[]

    for i in range(len(df2)):
        dj2.append(res(i))

### A function to invoke the llm. For some reason phi3 doesn't give accurate result sometimes if used directly in dj.append()
    def res2(i):
        response=chain.invoke({"question" : df2['Date + Desc'][i]+" Only name the type of vehicles involved in the accident. If multiple vehicles are involved, seperate them by hyphens(-). Example answers: Bus, Truck-Bus etc. If no vehicles are mentioned, your answer will be: Not Available. Your answer should only contain the vehicle name, do not include any extra sentences"})
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
        words = dj2[i].split(",")  # Splitting at the comma delimiter
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
    df3=df2.drop(columns=['Description','Date + Desc','Report Type'])
    return df3
    


