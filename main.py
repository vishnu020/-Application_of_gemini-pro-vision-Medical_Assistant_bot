import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
import os 

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Visual_Medical_Assistant",page_icon="🩺")
st.title("Medical Assistant bot 👨‍⚕️ 🩺 🏥")



generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 0,
                    "max_output_tokens": 8192,
                    }

safety_settings=[{'category':'HARM_CATEGORY_HARASSMENT',
                  'threshold':'BLOCK_MEDIUM_AND_ABOVE'},

                {'category':'HARM_CATEGORY_HATE_SPEECH',
                'threshold':'BLOCK_MEDIUM_AND_ABOVE'},

                {'category':'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                'threshold':'BLOCK_MEDIUM_AND_ABOVE'},

                {'category':'HARM_CATEGORY_DANGEROUS_CONTENT',
                    'threshold':'BLOCK_MEDIUM_AND_ABOVE'}]


system_prompts = [
                    """
                    You are a domain expert in medical image analysis. You are tasked with 
                    examining medical images for a renowned hospital.
                    Your expertise will help in identifying or 
                    discovering any anomalies, diseases, conditions or
                    any health issues that might be present in the image.
                    
                    Your key responsibilites:
                    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
                    focusing on finding any abnormalities.
                    2. Analysis Report : Document all the findings and 
                    clearly articulate them in a structured format.
                    3. Recommendations : Basis the analysis, suggest remedies, 
                    tests or treatments as applicable.
                    4. Treatments : If applicable, lay out detailed treatments 
                    which can help in faster recovery.
                    
                    Important Notes to remember:
                    1. Scope of response : Only respond if the image pertains to 
                    human health issues.
                    2. Clarity of image : In case the image is unclear, 
                    note that certain aspects are 
                    'Unable to be correctly determined based on the uploaded image'
                    3. Disclaimer : Accompany your analysis with the disclaimer: 
                    "Consult with a Doctor before making any decisions."
                    4. Your insights are invaluable in guiding clinical decisions. 
                    Please proceed with the analysis, adhering to the 
                    structured approach outlined above.
                    
                    Please provide the final response with these 4 headings : 
                    Detailed Analysis, Analysis Report, Recommendations and Treatments

                    
                    
                """
                ]

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts

model=genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                            generation_config=generation_config,
                            safety_settings=safety_settings)



uploaded_file=st.file_uploader("Upload the Image for the Medical Assistant",type=['png','jpg','jpeg'])

if uploaded_file:
    st.image(uploaded_file,width=200,caption="Uploaded Image by the User ")
submit=st.button("Genrate the analysis") 

if submit:
    image_parts=input_image_setup(uploaded_file)

    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]
    
#     generate response
    
    response = model.generate_content(prompt_parts)
    if response:
        st.subheader('Detailed analysis based on the uploaded image')
        st.write(response.text) 