import os
import streamlit as st
from groq import Groq
import fitz  # PyMuPDF
import docx

# Initialize Groq client with API key from Hugging Face environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit app
st.title("Job Application Cover Letter Generator")

st.write("Upload your CV and the job description to generate a customized cover letter.")

# Upload CV and Job Description
cv_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])
job_desc_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"])

def extract_text(file):
    """Extract text from a PDF or DOCX file."""
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        return None

def extract_text_from_pdf(file):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file using python-docx."""
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

if st.button("Generate Cover Letter"):

    if cv_file and job_desc_file:
        # Read the content of the files
        cv_text = extract_text(cv_file)
        job_desc_text = extract_text(job_desc_file)

        # Generate cover letter using Groq
        prompt = f"Using the following CV:\n{cv_text}\nand the job description:\n{job_desc_text}\nGenerate a tailored cover letter."

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        cover_letter = chat_completion.choices[0].message.content
        st.write("### Generated Cover Letter:")
        st.write(cover_letter)

    else:
        st.write("Please upload both a CV and a job description.")
