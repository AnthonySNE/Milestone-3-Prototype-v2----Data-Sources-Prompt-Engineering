from PyPDF2 import PdfReader
import openai
import os
import streamlit as st
from openai import OpenAI

st.markdown("# PDF Translator 📄🌐")
st.sidebar.markdown("# Page 3: Translation 🌐")

#Create two radio buttons for source and target languages
source_language = st.radio('Select Source language', ['English', 'French', 'German', 'Spanish', 'Chinese'])
target_language = st.radio('Select Target language', ['English', 'French', 'German', 'Spanish', 'Chinese'])

#Create a text input field for user input
text = st.text_input('Enter the text you want to translate: ')

#Function to translate text
def translate_text(text, source_language="English", target_language="French"):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI()

    # Customize the translation prompt
    prompt = ("You are provided with a text in " + source_language +
              ", and your task is to translate it into " + target_language + ".\n\n"
              "Original Text: " + text + "\n\n"
              "Translated Text:")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Update to the appropriate model
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1
    )

    return response.choices[0].message.content

#Function to translate PDF text
def translate_pdf(uploaded_file, source_language="English", target_language="French"):
    # Read the PDF file
    pdf_reader = PdfReader(uploaded_file)
    translated_pdf_text = ""

    # Extract text from each page and translate
    for page in pdf_reader.pages:
        text = page.extract_text()
        translated_pdf_text += translate_text(text, source_language, target_language) + "\n"

    return translated_pdf_text
    
st.write("OR")

#File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Translate the PDF text
    translated_pdf_text = translate_pdf(uploaded_file, source_language, target_language)

    # Display the translated text
    st.write("Translated Text:")
    st.write(translated_pdf_text)

#Function to display translated PDF text
def display_translated_pdf(uploaded_file, source_language="English", target_language="French"):
    # Translate the PDF text
    translated_pdf_text = translate_pdf(uploaded_file, source_language, target_language)

#Display the translated text
    st.write("Translated PDF Text:")
    st.write(translated_pdf_text)

#Button to display translated PDF text
if st.button("Display Translated PDF Text"):
    if uploaded_file is not None:
        display_translated_pdf(uploaded_file, source_language, target_language)
    else:
        st.write("Please upload a PDF file first.")
