from dotenv import load_dotenv

load_dotenv()# load all the enviroment variablesfrom .env

import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai


# test ssh config 
# test 2 ssh config with the right user 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

## Function to load Gemini Pro Vision
model = genai.GenerativeModel("gemini-1.5-pro")  # or "gemini-1.5-flash"


def get_gemini_response(input_prompt,image, prompt):
    # input_prompt --> telling the model what should do ! in this case it s the extraction of data 
    # prompt --> is what information i want to extract .
    # image --> is the input we want to extract data from .
    response=model.generate_content([input_prompt,image[0],prompt])
    return response.text

def process_image(uploaded_document):
    if uploaded_document is not None:
        data  = uploaded_document.getvalue()
        data_type =  uploaded_document.type
        image_data = [
            {
                "mime_type" : data_type, 
                "data" : data 
            }
        ]
        return image_data
    else: 
        raise FileNotFoundError("No file uploaded")

## initialize the streamlit app 
st.set_page_config(page_title="MY Invoice Extractor")
st.header("Gemini Vision Pro")
prompt = st.text_input("Input_prompt: ", key="input")
uploaded_file =st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
img= ""
if uploaded_file is not None:
    img=Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

submit =st.button("Tell me about the document")
input_prompt = """
You are an expert in analyzing CVs.
You will receive an image of a resume and extract details about the person.
"""

if submit:
    image_input = process_image(uploaded_document=uploaded_file)
    response =get_gemini_response(input_prompt=input_prompt, image=image_input, prompt= prompt)
    st.subheader("the Response is")
    st.write(response)