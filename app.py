import streamlit as st
import pandas as pd
from PIL import Image
import json
from streamlit_lottie import st_lottie

##### BUET Logo ###########
image = Image.open("buet.png")
new_image = image.resize((100, 100))
#st.image(new_image)
st.title("Automated LLM and Web Scrapping based Road Accident Dataset creation from Newspapers")


######### Animation ##########
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_coding=load_lottiefile("animate.json")
st_lottie(
        lottie_coding,
        height=200,
        
    )


radio_btn1=st.radio("**Choose the newspaper you want to collect news from**",options=("Prothom Alo","Dhaka Tribune","The Daily Star"))
radio_btn2=st.radio("Choose an LLM model",options=("GPT-3.5 (Medium Cost)","GPT-4 (High Cost)","Llama3 (Free)"))

number = st.number_input("**Enter the number of accident news you want the LLM to go through**",min_value=0,max_value=5000)

if st.button("Generate Dataset"):
    st.write("**Please wait until the datasest is finished generating. It takes almost 8 sec to process each entry for GPT-4 and 30 sec for GPT-3.5 and Llama3. So, for example, if you entered 15 as input, it will take almost 2 minutes for GPT-4 and 7.5 min for GPT-3.5 and Llama3. The dataset will appear below.**")
    
    if radio_btn1=="Prothom Alo":
        import Prothom_alo_fully_scraped
        df=Prothom_alo_fully_scraped.get_data(number)
    elif radio_btn1=="Dhaka Tribune":
        import Dhaka_Tribune_Fully_Scraped
        df=Dhaka_Tribune_Fully_Scraped.get_data(number)
    elif radio_btn1== "The Daily Star":
        import Daily_Star_fully_scraped
        df=Daily_Star_fully_scraped.get_data(number)
    if radio_btn2=="GPT-4 (High Cost)":
        import LLM_automation_GPT
        df2=LLM_automation_GPT.create_data(df)
    elif radio_btn2=="Llama3 (Free)":
        import LLM_automation_Groq
        df2=LLM_automation_Groq.create_data(df)
    elif radio_btn2=="GPT-3.5 (Medium Cost)":
        import LLM_automation_GPT35
        df2=LLM_automation_GPT35.create_data(df)
    st.dataframe(df2)
    print(len(df))
    
    
#st.write("""
#                    **Developed by:**\n
        
#                    *MD Thamed Bin Zaman Chowdhury, Student ID: 1904184,*\n
#                    *Department of Civil Engineering, BUET*\n
#                    *E-mail: zamanthamed@gmail.com*
#         """)


st.write("--------")
st.write("**Modules and packages used to develop the program:**")

######## Other Logos ################
p=125
image2 = Image.open("pandas.png")
new_image2 = image2.resize((p, p))
image3 = Image.open("numpy.png")
new_image3 = image3.resize((p, p))
image4 = Image.open("selenium_webdriver.jpeg")
new_image4 = image4.resize((p, p))
image5 = Image.open("streamlit.png")
new_image5 = image5.resize((p, p))
image6 = Image.open("openai.png")
new_image6 = image6.resize((p, p))
image7 = Image.open("llama3.jpeg")
new_image7 = image7.resize((p, p))
image8 = Image.open("langchain.png")
new_image8 = image8.resize((p, p))
image9 = Image.open("deep_translator.png")
new_image9 = image9.resize((p, p))

st.image([new_image2, new_image3,new_image4,new_image5,new_image6,new_image7,new_image8,new_image9])