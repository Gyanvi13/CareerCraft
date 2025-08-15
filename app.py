
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2

# Load environment variables 
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Using a more recent and powerful model is often a good idea
model = genai.GenerativeModel('gemini-1.5-pro-latest') 


def get_gemini_response(prompt):
    """Get AI response safely from Gemini."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠ API call failed: {e}"

def extract_pdf_text(uploaded_file, max_chars=2000): # Increased max_chars slightly
    """Extract and truncate PDF text to avoid large prompts."""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        # Ensure text is not empty before returning
        return text[:max_chars] if text else ""
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None


input_prompt = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing
Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App
Developer, Devops Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect,
Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX
Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess
resumes against provided job descriptions. Assign precise matching percentages and identify missing keywords.

resume: {text}
description: {jd}

I want the response in the following structure and nothing else:
MATCH_PERCENTAGE:
<MATCH PERCENTAGE>

MISSING_KEYWORDS:
<comma-separated keywords>

PROFILE_SUMMARY:
<A concise summary highlighting skills and experience>
"""


st.set_page_config(page_title="CareerCraft", layout="wide")
st.markdown("""
<style>
.section-title { text-align: center; font-size: 28px; font-weight: bold; color: #4CAF50; margin-bottom: 20px; }
.offer-item { background-color: #f0f0f0; padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 16px; }
.highlight { background-color: #e0f7fa; padding: 20px; border-radius: 8px; border: 1px solid #4CAF50; }
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: #4CAF50;'>CareerCraft 🚀</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Optimize your resume and find your dream job!</h3>", unsafe_allow_html=True)
st.divider()

st.markdown("<div class='section-title'>🌟 What We Offer</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
offerings = [
    "ATS-Optimized Resume Analysis",
    "Resume Optimization",
    "Skill Enhancement",
    "Career Progression Guidance",
    "Tailored Profile Summaries",
    "Streamlined Application Process",
    "Personalized Recommendations",
    "Efficient Career Navigation"
]

for i, col in enumerate([col1, col2, col3, col4]):
    for j in range(i, len(offerings), 4):
        col.markdown(f"<div class='offer-item'>✅ {offerings[j]}</div>", unsafe_allow_html=True)

st.divider()


st.markdown("<div class='section-title'>🧭 Embark on Your Career Adventure</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    jd = st.text_area("📄 Paste the Job Description", height=250)
    uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type="pdf")
    if st.button("🔍 Analyze Resume"):
        if uploaded_file and jd.strip():
            with st.spinner("AI is analyzing your resume... Please wait."):
                resume_text = extract_pdf_text(uploaded_file)
                if resume_text is not None: # Check if PDF extraction was successful
                    prompt = input_prompt.format(text=resume_text, jd=jd)
                    response = get_gemini_response(prompt)
                    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
                    st.subheader("📊 AI Analysis Result")
                    st.markdown(response.replace("MATCH_PERCENTAGE:", "**MATCH PERCENTAGE:**").replace("MISSING_KEYWORDS:", "\n**MISSING KEYWORDS:**").replace("PROFILE_SUMMARY:", "\n**PROFILE SUMMARY:**"))
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("⚠ Please provide both a Job Description and a Resume.")

with col2:
    st.metric("Total Resumes Analyzed", "1,245", delta="+12 today")
    st.metric("Successful Matches", "892", delta="72% success rate")

st.divider()


st.markdown("<div class='section-title'>❓ Frequently Asked Questions</div>", unsafe_allow_html=True)
with st.expander("How does CareerCraft analyze resumes and job descriptions?"):
    st.write("CareerCraft uses advanced Google Gemini AI to perform semantic matching of skills, experience, and keywords from your resume against the provided job description.")
with st.expander("Can CareerCraft suggest improvements for my resume?"):
    st.write("Yes! By highlighting the missing keywords, CareerCraft gives you direct insights on what to add to your resume to better align with the job and pass through Applicant Tracking Systems (ATS).")
with st.expander("Is CareerCraft suitable for both entry-level and experienced professionals?"):
    st.write("Absolutely! The analysis is based on the provided job description, making it a valuable tool for professionals at any stage of their career.")

st.markdown("<h3>📚 Tips for Job Seekers</h3>", unsafe_allow_html=True)
st.write("- Keep your resume clear and concise.")
st.write("- Highlight measurable achievements using numbers and data.")
st.write("- Use keywords from the job description naturally within your experience bullet points.")
st.write("- Tailor your resume for each application to maximize your match percentage.")
