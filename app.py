from dotenv import load_dotenv

load_dotenv()

from PIL import Image
import fitz  # PyMuPDF
import os
import io
import base64
import google.generativeai as genai
import streamlit as st
import pdf2image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Or hardcode for testing

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
    final_prompt = f"{prompt}\n\n{input_text}\n\n{pdf_content}"
    response = model.generate_content(final_prompt)
    return response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text


def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    else:
        raise FileNotFoundError("No file uploaded.")

## stream lit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ",key = "input")
uploaded_file = st.file_uploader("upload your resume(PDF)...",type = ["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded sucessfully")

submit1 = st.button("Tell me About the resume")
submit2 = st.button("How can I Improvise my Skills")
submit3 = st.button("What are the keywords That are Missing")
submit4 = st.button("percentage Match")

input_prompt1 = """
You are a professional ATS (Applicant Tracking System) and Resume Analyzer. Analyze the following resume.

Extract and organize the following fields:
1. Full Name
2. Contact Information
3. LinkedIn / GitHub (if any)
4. Summary or Career Objective
5. Technical Skills (Programming Languages, Tools, Technologies)
6. Educational Background (degrees, colleges, years)
7. Work/Internship Experience (role, company, duration, key points)
8. Certifications (with issuer and year)
9. Academic/Personal Projects (title, description, tech stack)
10. Soft Skills / Communication Skills
11. Awards / Achievements
12. Extracurricular Activities
13. Keywords extracted from resume (important for ATS)
14. Formatting & structure feedback

Also include:
- Based on the resume, suggest 3–5 **suitable job roles** (e.g., "Data Analyst", "Backend Developer", "DevOps Intern")
- Mention why each job role suits the candidate based on skills/experience
"""
input_prompt2 = """
You are an ATS-based skill gap analyst. Evaluate the resume and provide detailed suggestions on **how the candidate can improve their skills**.

Follow this structure:
1. Current Technical Skills identified
2. Important Skills Missing (based on current industry expectations)
3. Soft Skills missing or underrepresented
4. Certifications or courses the candidate can pursue
5. Relevant Tools or Libraries the candidate should learn
6. Suggest 2–3 career paths with skill maps (e.g., "To become a Data Scientist, learn: Python, Pandas, Scikit-learn, SQL, etc.")
7. Suggest online platforms or certifications (Coursera, Udemy, LinkedIn Learning)

End with:
- Personalized skill-building roadmap (beginner ➝ intermediate ➝ advanced)
"""

input_prompt3 = """
Act like an ATS keyword scanner.

1. Extract all **keywords** currently present in the resume
2. Compare with industry-standard keywords for common roles like:
   - Software Developer
   - Data Analyst
   - Frontend Developer
   - Backend Developer
   - Machine Learning Engineer
3. List all **missing but important keywords** not found in the resume
4. Suggest where/how to include these keywords naturally in:
   - Skills section
   - Project descriptions
   - Experience bullets
5. Highlight any unnecessary or overused buzzwords
6. Provide a restructured **Keywords Enhancement Table** (with "Missing", "Importance", "Where to add")

Also recommend best-fit job roles based on existing and missing keywords.
"""


input_prompt4 = """
You are a strict ATS engine. Match the resume against the job description below and give a detailed report.

Return:
1. **Overall ATS Match Score** (out of 100%)
2. **Match Breakdown**:
   - Skills Match %
   - Experience Match %
   - Education Match %
   - Keywords Match %
   - Project Relevance %
3. List all matched keywords
4. List missing or weak keywords
5. Suggest improvements to increase score
6. Based on the match, suggest if the candidate fits:
   - Excellent Match (90–100%)
   - Good Match (70–89%)
   - Moderate (50–69%)
   - Poor (<50%)

Also give:
- Role Suitability: Which roles this resume fits best
- Confidence Score for each suggested role
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload a resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt2)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload a resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt3)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload a resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt4)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload a resume")














