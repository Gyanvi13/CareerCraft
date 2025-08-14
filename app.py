
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')

def get_gemini_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error generating response: {e}"

def input_pdf_text(upload_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(upload_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

input_prompt = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing
Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App
Developer, Devops Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect,
Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX
Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess
resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial
in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD
(Job Description) and meticulously identify any missing keywords with utmost accuracy.

resume: {text}
description: {jd}

I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.
Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""

st.set_page_config(page_title="CareerCraft", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .section-title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #4CAF50;
        }
        .offer-item {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# First section
col1, col2 = st.columns([3, 2])
with col2:
    st.markdown("<div class='section-title'>🌟 Wide Range of Offerings</div>", unsafe_allow_html=True)
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
    for item in offerings:
        st.markdown(f"<div class='offer-item'>✅ {item}</div>", unsafe_allow_html=True)

with col1:
    st.markdown("### 📌 Career Growth & Opportunities")
    st.markdown("Find your perfect job match with AI-powered resume analysis & career guidance.")
    st.progress(80)
    st.info("🚀 Ready to level up your career? Let's start!")

st.divider()

# Second section - JD & Resume Input
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<div class='section-title'>🧭 Embark on Your Career Adventure</div>", unsafe_allow_html=True)
    jd = st.text_area("📄 Paste the Job Description")
    uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type="pdf", help="Please upload a PDF file")

    if st.button("🔍 Submit for Analysis"):
        if uploaded_file is not None and jd.strip() != "":
            st.success("✅ Resume and JD submitted successfully! AI is analyzing...")

            # Extract resume text
            resume_text = input_pdf_text(uploaded_file)

            # Prepare prompt
            prompt = input_prompt.format(text=resume_text, jd=jd)

            # Get AI response
            response = get_gemini_response(prompt)

            st.subheader("📊 AI Analysis Result")
            st.write(response)
        else:
            st.error("⚠ Please provide both a Job Description and a Resume.")

with col2:
    st.metric(label="Total Resumes Analyzed", value="1,245", delta="+12 today")
    st.metric(label="Successful Matches", value="892", delta="72% success rate")
    image_url = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    try:
       st.image(image_url, use_container_width=True)
    except Exception:
        st.warning("Profile image unavailable.")

st.divider()

# Third section - FAQ
col1, col2 = st.columns([2, 3])
with col2:
    st.markdown("<div class='section-title'>❓ Frequently Asked Questions</div>", unsafe_allow_html=True)
    with st.expander("How does CareerCraft analyze resumes and job descriptions?"):
        st.write("CareerCraft uses advanced algorithms to match skills and keywords from your resume with the job description.")
    with st.expander("Can CareerCraft suggest improvements for my resume?"):
        st.write("Yes! CareerCraft provides personalized recommendations to help you stand out.")
    with st.expander("Is CareerCraft suitable for both entry-level and experienced professionals?"):
        st.write("Absolutely! CareerCraft caters to job seekers at all career stages.")

with col1:
    st.markdown("### 📚 Tips for Job Seekers")
    st.write("- Keep your resume clear and concise")
    st.write("- Highlight measurable achievements")
    st.write("- Use keywords from the job description")