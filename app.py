import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
import openai
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import AzureOpenAI
import time
import altair as alt

#load environment variables
load_dotenv(find_dotenv(), override=True)

# Read tge reqyured environment variables
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = os.environ.get('OPENAI_DEPLOYMENT_ENDPOINT')  
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are SmartAI, a helpful assistant. You are helping a user find a house to buy. The user asks you questions about the house and you answer them. If you can not answer the question, you can say I don't know answer to your question and apologise to them."}
    ]

with st.sidebar:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    Endpoint = st.text_input('API Endpint', 'https://pikachudoesgenai.openai.azure.com/openai')
    st.write("")
    st.write("")
    APIKey = st.text_input('Azure API Key', '857dfb446de24b73a949ea31a36c13a3')
    st.write("")
    st.write("")
    st.button("Save")

def main():

    st.title("AI Powered Real Estate Platform")
    st.write("")
    st.write("")

    # Create tabs
    tab_titles = ['Predict', 'Explore']
    tabs = st.tabs(tab_titles)

    df = pd.read_csv('Cleansed_USA_Housing.csv')

    dfllm = AzureOpenAI(api_token=os.environ['OPENAI_API_KEY'],
                api_base=os.environ['OPENAI_DEPLOYMENT_ENDPOINT'],
                api_version=os.environ["OPENAI_API_VERSION"],
                deployment_name="gpt-4",
                temperature=0,
                api_type=os.environ['OPENAI_API_TYPE'],
                is_chat_model=True)

    df = SmartDataframe(df, config={"llm": dfllm})

    with tabs[0]:
        AreaIncome = st.number_input('Area Income?', min_value=0, max_value=200000, value=0, step=1)
        HouseAge = st.slider('House Age?', 0, 50, 1)
        BedRoomCount = st.slider('Bed room count?', 0, 10, 1)
        BedRoomArea = st.slider('Bed room area?', 0, 50, 1)
        AreaPopulation = st.number_input('Population of Area?', min_value=0, max_value=1000000, value=0, step=1)

        button = st.button("Predict")

        if button:
            #question = f"Can you Predict the price of a house with {BedRoomCount} bedrooms, {BedRoomArea} bed room area, {HouseAge} years old, {AreaIncome} income and {AreaPopulation} population"
            question = f"What could be the average price for a house with {BedRoomCount} bedrooms, {HouseAge} years old, {AreaIncome} income and {AreaPopulation} population"
            #question = f"What could be the average price for a house with {BedRoomCount} bedrooms, {HouseAge} years old, {AreaIncome} income, {AreaPopulation} population and {BedRoomArea} bed room area"
            #question  = "What could be the average price for 3 bedroom house which is 5 years old in area like 8108?"
            
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(5)

            for percent_complete in range(1):
                time.sleep(0.01)
                response = df.chat(question)
            my_bar.progress(100)
            st.write(response)

            st.line_chart(df[["Avg. Area Income","Avg. Area House Age", "Avg. Area Number of Rooms", "Avg. Area Number of Bedrooms", "Area Population"]])

            c = alt.Chart(df).mark_circle().encode(
                x='Price', y='Avg. Area Income', size='Avg. Area House Age', color='c', tooltip=['Price', 'Avg. Area Income', 'Avg. Area House Age'])
            #st.altair_chart(c, use_container_width=True)

    
    with tabs[1]:
        st.title("Hey, I am SmartAI.!")
        st.write("How can I assist you today?")

        container = st.container()
        response_container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_area("Enter your question here", height=100, key='input')
                submit_button = st.form_submit_button(label='Send')

                if submit_button:
                    output = df.chat(user_input)
                    output = str(output)
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output)

                    with response_container:
                        if st.session_state['generated']:
                            for i in range(len(st.session_state['generated'])):
                                st.write("You: " + st.session_state['past'][i])
                                st.write("  SmartAI: " + str(st.session_state['generated'][i]))




if __name__ == '__main__':
    main()

