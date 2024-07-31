# Web Scraping and Large Language Models (LLM) Based Automated Accident Dataset Generation
This is a web scraping and LLM based application that can collect and process accident news automatically and generates an excel file.
## Introduction
Welcome to this github repo. This project aims to generate accident dataset fully automatically. First, the program visits a newspaper website the user has specified. Then it collects accident news automatically using selenium. Then the collected news is processed through an LLM specified by the user to generate accident dataset. Currently, this application can scrape news from 3 websites in Bangladesh: 'The Prothom Alo', 'The Daily Star' and 'Dhaka Tribune'. The user has a choice of using any of the 3 LLMS: GPT-4, GPT-3.5 and Llama3. This dataset will be useful for building Machine Learning models and policy decision making.
This project was built as part of a thesis work by the author. So, if you are intersted to know details, you may read this paper. Anyone is welcome to use this work but please cite this paper if you are benefitted from it.
## How to use?
There are two ways to use this program:
  1) Using it as a web application
  2) Using this locally in user's PC
The explanation of each way is given below:
### Using it as a web application
The authors built this work as a streamlit application and hosted it on huggingface spaces. If you want to see a demo of this work, it is strongly recomended to use this method. 
Steps:
1) Go to this link:
   (https://huggingface.co/spaces/Thamed-Chowdhury/Automated_Accident_Dataset)
3) You will be seeing an interface like this.
   !![image](https://github.com/user-attachments/assets/60865c55-988d-442f-bbe9-8c43b7b01404)

5) Choose a newspaper you want to collect news from.
6) Choose an LLM you want to process the news with.
7) You have to wait some minutes depending on your input as it takes some time.
8) You will be seeing the generated dataset once the process is finished and download it as a CSV file.

Disclaimer: Since this is only a demo for this work, it has some limitations. It does not provide the users the option to collect news from "Dhaka Tribune" newspaper. Also, since there are cost involved in using the LLMs, maximum 50 news reports can be processed. If you want to avoid these limitations, follow the 2nd method.

### Using this locally in user's PC
This method is for those who want to run the application in their own pc and avoid the limitations of 1st method. The steps are given below. Note that we are using anaconda for this purpose:
1) Download this repo and unzip it in a folder.
2) Open Anaconda Prompt and navigate to the folder where the folder is located.
1) Create a virtual environment using anaconda. The virtual environment must be using python 3.12.3. Here we are giving an example. Note that during this whole process, anaconda might ask for permissions several times. You have to type "y" in these cases and press enter.
2) Activate the virtual environment in anaconda and install the dependencies stated in requirements.txt file.
3) Once the installation is completed, type in the anaconda prompt the following command:
   ```
   streamlit run app.py
   ```
4) If everything is successful, a browser window will open up containing the web app as shown below.
5) Now, you are done! You can collect accident data as your heart's content 😉

# Please cite our paper if this work helps you in any way. Thanks. 💓
