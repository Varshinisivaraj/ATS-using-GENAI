import google.generativeai as genai
import pdf2image
import io
import time
import streamlit as st
import base64

GOOGLE_API_KEY = "AIzaSyDECC7_txdv226Tdk3eIB_MhveIIp7xsXM"
genai.configure(api_key=GOOGLE_API_KEY)


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                # encode to base64
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App


st.set_page_config(page_title="ARTS Resume Expert")
st.header("ARTS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_files = st.file_uploader("Upload your resume (PDF)...", type=[
                                  "pdf"], accept_multiple_files=True)

if uploaded_files is not None:
    st.write("PDF Uploaded Successfully")


input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of Data Science,Data Analyst,Data Engineer,Full stack wen development,DEVOPS,
 your task is to review the provided resume against the job description for these profiles. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are developing a chatbot to assist with resume shortlisting. The chatbot needs to evaluate resumes against job descriptions and 
provide a percentage match. As an expert in Applicant Tracking Systems (ATS) and with a deep understanding of data science, data analysis, 
data engineering, full-stack web development, and DevOps, your task is to assess the provided resume against the given job description.
First, the output should be the percentage match between the resume and job description. Then, list any keywords missing from the resume 
content. Finally, provide any additional thoughts or considerations. Ensure that the percentage is distinct for each resume. If any keywords
from the job description do not match the resume content, the percentage should be 0 or less than 60.
""" 

if len(uploaded_files) == 1:
    submit1 = st.button("Tell Me About the Resume")
    submit3 = st.button("Percentage Match")

    if submit1:
        if uploaded_files is not None:
            pdf_content = input_pdf_setup(uploaded_files[0])
            response = get_gemini_response(
                input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    if submit3:
        if uploaded_files is not None:
            pdf_content = input_pdf_setup(uploaded_files[0])
            response = get_gemini_response(
                input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

if len(uploaded_files) > 1:
    about_resumes = {}
    percentage_match = {}

    for uploaded_file in uploaded_files:
        pdf_content = input_pdf_setup(uploaded_file)
        about_resumes[uploaded_file.name] = get_gemini_response(
            input_prompt1, pdf_content, input_text)
        percentage_match[uploaded_file.name] = get_gemini_response(
            input_prompt3, pdf_content, input_text)
        time.sleep(1)

    resume_name = st.selectbox(
        "Choose Resume for Details", options=about_resumes.keys())
    st.subheader("Details of the Chosen Resume")
    st.write(about_resumes[resume_name])
    st.subheader("Percentage Match of the Chosen Resume")
    st.write(percentage_match[resume_name])
