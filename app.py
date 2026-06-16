import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Title
st.title("📄 AI Resume Analyzer")

st.write("Upload your resume and get AI feedback.")

# Upload resume
# Upload resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    # Read PDF
    pdf_reader = PdfReader(uploaded_file)

    text = ""

    # Extract text
    for page in pdf_reader.pages:
        text += page.extract_text()

    with st.expander("📄 View Resume Text"):
        st.write(text[:3000])

    # Role selector
    target_role = st.selectbox(
        "🎯 Select Target Role",
        [
            "AI Engineer",
            "Data Scientist",
            "ML Engineer",
            "Software Engineer",
            "Data Analyst"
        ]
    )

    # ADD THIS HERE ↓↓↓
    job_description = st.text_area(
        "📄 Paste Job Description (Optional)",
        height=200
    )

    # Analyze button
    if st.button("Analyze Resume"):

        with st.spinner("Analyzing resume..."):

            response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a brutally honest ATS recruiter and hiring manager.

Target Role:
{target_role}

If a job description is provided,
compare the resume against it.

Identify:
- Matching skills
- Missing skills
- Resume gaps
- ATS keyword match

DO NOT summarize the resume.
CRITIQUE IT and don't sugarcoat it.
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
Resume:

{text}

Job Description:

{job_description}
"""
                    }
                ]
            )

            analysis = response.choices[0].message.content

            st.subheader("📋 Resume Analysis")
            st.markdown(analysis)