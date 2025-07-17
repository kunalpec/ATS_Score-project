# Field to pu my jd
# upload pdf
#  pdf tp image...>processing----->google gemini pro
# prompts templates nedd to create
# give data to user

from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
import io
import pandas as pd
import base64
from PIL import Image
import pdf2image
import pdfplumber
import google.generativeai as genai

genai.configure(api_key=st.secrets["API_KEY"])

def get_gemini_response(input,pdf_content,prompt):
  model=genai.GenerativeModel('gemini-1.5-flash')
  response=model.generate_content([input,pdf_content[0],prompt])
  return response

import base64
import io
from pdf2image import convert_from_bytes


def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text
# streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

# condition
if uploaded_file is None:
    st.write("PDF Uploaded Successfully")

submit1=st.button("Tell Me About The Resume")
submit2=st.button("How Can I Improvise my Skills")
# submit3=st.button("What are the Keyworlds that are Missing")
submit3=st.button("Percentage match")
submit4=st.button("Show Statistic Knowledge")


input_propt1="""You are a senior HR specialist with strong technical expertise and extensive experience of any one job role in the fields of Data Science, Full Stack Development, Web Development, and Big Data Engineering. You are highly skilled in both recruitment processes and technical evaluations.
Your task is to thoroughly assess the candidate's resume in relation to the provided job description. Carefully analyze the applicant’s educational background, work experience, technical skills, certifications, and notable achievements.
Based on this comparison, provide a detailed and professional evaluation of how well the candidate aligns with the job requirements. Clearly highlight key strengths, relevant skills, and accomplishments that support the applicant’s suitability for the role. Additionally, point out any weaknesses, missing qualifications, or skill gaps that could be areas of concern for the hiring team.
Your response should conclude with a clear hiring recommendation (e.g., Strong Fit, Partial Fit, or Not a Good Fit) along with a brief explanation to support your decision,also tell the strength and weakness of candidate. Please maintain a formal and objective tone throughout the review to reflect a real-world HR assessment.
"""

input_propt2="""
You are a Technical Human Resources Manager with expertise of any one job role data science and  Full Stack Development, Web Development, and Big Data Engineering.. Your task is to thoroughly evaluate the candidate’s resume based on the provided job description. Analyze the candidate’s qualifications, skills, experience, and achievements to determine how well they align with the role. Provide a detailed assessment highlighting the candidate’s strengths, relevant accomplishments, and any areas where qualifications may be lacking. Offer constructive advice for improving their profile, and conclude with a clear hiring recommendation such as Strong Fit, Partial Fit, or Not a Good Fit. Maintain a formal and objective tone throughout your review to simulate a real-world HR evaluation.
with Addition to that please tell to the condidate ,what it needs to work upon on their Skills.
"""

input_propt3="""
You are a highly advanced AI-based Applicant Tracking System (ATS) scanner with deep understanding of job roles, skills, and recruitment standards. Your task is to evaluate the provided resume against the given job description. First, calculate and return a percentage score indicating how well the candidate’s profile matches the job requirements. Then, provide a detailed analysis highlighting the strengths and key skills that align with the job, as well as any weaknesses or missing qualifications. Ensure your evaluation is clear, structured, and professional, simulating a real-world ATS screening process used by hiring teams.
"""

input_prompt4 = """
You are analyzing a resume and a job description.

Step 1: Extract all technical or domain subjects explicitly listed in the job description.

Step 2: For each subject in the job description, check the resume and assign an accurate proficiency percentage (0% to 100%) based strictly on the presence and detail of that subject in the resume.

- If the subject appears clearly with good detail, assign a high percentage.
- If the subject appears but with little or vague detail, assign a low percentage (minimum 10%).
- If the subject does not appear at all in the resume, assign exactly 0%.
- Do not include any subjects that are not in the job description.
- Include all job description subjects in the output, even if the percentage is 0%.

Return only the subjects and their percentages in this exact format, with each subject on its own line:

<Subject> <Percentage>%

Do not add any explanation, comments, or additional text.

Example:
Python 80%
SQL 65%
Power BI 50%
Machine Learning 75%
"""



if submit1:
    if uploaded_file is not None:
        pdf_content=extract_text_from_pdf(uploaded_file)
        # input,pdf_content,prompt
        response=get_gemini_response(input_propt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response.text)
    else:
        st.warning("Please Upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=extract_text_from_pdf(uploaded_file)
        # input,pdf_content,prompt
        response=get_gemini_response(input_propt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response.text)
    else:
        st.warning("Please Upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=extract_text_from_pdf(uploaded_file)
        # input,pdf_content,prompt
        response=get_gemini_response(input_propt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response.text)
    else:
        st.warning("Please Upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content=extract_text_from_pdf(uploaded_file)
        response =get_gemini_response(input_prompt4,pdf_content,input_text) 
        # Parse Gemini output
        subjects = []
        percentages = []
    
        for line in response.text.strip().split("\n"):
            try:
                subject, percent = line.rsplit(" ", 1)
                percent = int(percent.replace("%", ""))
                subjects.append(subject)
                percentages.append(percent)
            except:
                continue
              
        df = pd.DataFrame({"Subject": subjects, "Proficiency (%)": percentages})
        st.subheader("Your Subject-wise Knowledge With Respect To (Resume & JD)")
        st.bar_chart(df.set_index("Subject"))
