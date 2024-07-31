# Web Scraping and Large Language Models (LLM) Based Automated Accident Dataset Generation
This is a web scraping and LLM based application that can collect and process accident news automatically and generates an excel file.
## Introduction
Welcome to this github repo. This project aims to generate accident dataset fully automatically. First, the program visits a newspaper website the user has specified. Then it collects accident news automatically using selenium. Then the collected news is processed through an LLM specified by the user to generate accident dataset. Currently, this application can scrape news from 3 websites in Bangladesh: 'The Prothom Alo', 'The Daily Star' and 'Dhaka Tribune'. The user has a choice of using any of the 3 LLMS: GPT-4, GPT-3.5 and Llama3. This dataset will be useful for building Machine Learning models and policy decision making.
This project was built as part of a thesis work by the author. So, if you are intersted to know details, you may read this paper. Anyone is welcome to use this work but **please cite this paper if you are benefitted from it.**
## How to use?
There are two ways to use this program:
  1) Using the app as a web application
  2) Using the app locally in user's PC

The explanation of each way is given below:
### Using it as a web application
The authors built this work as a streamlit application and hosted it on huggingface spaces. If you want to see a demo of this work, it is strongly recomended to use this method. 

Steps:

1) Go to this link:
   (https://huggingface.co/spaces/Thamed-Chowdhury/Automated_Accident_Dataset)
2) You will be seeing an interface like this.
   ![image](https://github.com/user-attachments/assets/60865c55-988d-442f-bbe9-8c43b7b01404)

3) Choose a newspaper you want to collect news from.
4) Choose an LLM you want to process the news with.
5) Click 'Generate Dataset' button
6) You have to wait some minutes depending on your input as it takes some time.
7) You will be seeing the generated dataset once the process is finished and download it as a CSV file.
   ![image](https://github.com/user-attachments/assets/ee4d6921-1af6-40cf-81af-a1f8a0552ae1)


**Disclaimer**: Since this is only a demo for this work, it has some limitations. It does not provide the users the option to collect news from "Dhaka Tribune" newspaper. Also, since there are cost involved in using the LLMs, maximum 50 news reports can be processed. If you want to avoid these limitations, follow the 2nd method.

### Using this locally in user's PC
This method is for those who want to run the application in their own pc and avoid the limitations of 1st method. The steps are given below. Note that we are using anaconda for this purpose:

1) Download this repo and unzip it in a folder.
2) To use this app locally in your PC, you will be requiring two API keys: one from OpenAI and another from Groq. You have to make some changes in the files downloaded using these keys. The steps are given below:
   i) Open the "LLM_automation_GPT" python file. In line 17, paste your OpenAI API key inside the quotations as shown below. Then save and close the file:
   ![image](https://github.com/user-attachments/assets/803a8e51-bf2a-4d07-9a66-6d154cb9b496)

   ii) Now open the "LLM_automation_GPT35" python file. Go to line 15 and paste your OpenAI API key as shown. Save and close the file.
   ![image](https://github.com/user-attachments/assets/8355a0f1-e049-4179-9b3c-3cddd0ba7364)

   iii) Now open the "LLM_automation_Groq" python file. Go to line 17 and paste your Groq API key as shown. Save and close the file.
   ![image](https://github.com/user-attachments/assets/c7d2a5f4-2133-43ec-9977-c7cad1555728)


3) Next open Anaconda Prompt and navigate to the folder where the folder is located.
4) Create a virtual environment using anaconda. The virtual environment must be using python 3.12.3. Here we are giving an example. Note that during this whole process, anaconda might ask for permissions several times. You have to type "y" in these cases and press enter. Note that in this example, we are naming our virtual environment `Accident_env` and making sure our python version is 3.12.3. To create a virtual environment run the following command in Anaconda Prompt:
   ```
   conda create -n Accident_env python=3.12.3 anaconda
   ```
   ![image](https://github.com/user-attachments/assets/18e70cfd-f19c-431f-928d-06c94f4d59cf)
   
5) After creating the virtual environment, we must activate the virtual environment in anaconda and install the dependencies stated in requirements.txt file using pip. To activate the virtual environment and install dependencies, run the following commands in Anaconda Prompt:
   ```
   conda activate Accident_env
   pip install -r requirements.txt
   ```
   If the installation is successful, a window similar to the image below should appear:
   ![image](https://github.com/user-attachments/assets/5f502510-2225-4fcc-83a4-737f198f5332)

6) Once the installation is completed, type in the anaconda prompt the following command:
   ```
   streamlit run app.py
   ```
7) If everything is successful, a browser window will open up containing the web app as shown below.
   ![image](https://github.com/user-attachments/assets/41c30210-64a5-4863-8fe9-f8a6cb90e42b)

8) Now, you are done! You can collect accident data as your heart's content 😉

# Please cite our paper if this work helps you in any way. Thanks. 💓
