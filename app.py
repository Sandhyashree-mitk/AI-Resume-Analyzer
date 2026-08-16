import streamlit as st
import pdfplumber
import plotly.express as px
import plotly.graph_objects as go

from history import save_history
from dashboard import show_dashboard
from course_recommender import recommend_courses

from parser import (
    extract_name,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
    extract_skills,
    extract_education,
    extract_certifications
)

from ats import (
    calculate_ats_score,
    get_resume_suggestions
)

from matcher import match_resume
from section_analyzer import analyze_sections
from report_generator import generate_report

from resume_rewriter import (
    improve_summary,
    improve_project,
    improve_experience,
    generate_bullets,
    recommend_skill_improvements,
    analyze_resume_for_job
)



# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📄 AI Resume Analyzer")

    st.write("### 🧭 Navigation")

    page = st.radio(
    "Go to",
    [
        "🏠 Home",
        "📊 Dashboard",
        "🤖 AI Resume Assistant"
    ]
)

    st.info(
        "Upload your resume and analyze your "
        "ATS score, skills, job match and improvements."
    )

    st.divider()

    st.write("### 🚀 Features")

    st.write("✅ ATS Resume Scoring")
    st.write("✅ Skill Analysis")
    st.write("✅ Job Matching")
    st.write("✅ Course Recommendations")
    st.write("✅ AI Resume Analysis")
    st.write("✅ PDF Report")

    st.divider()

    st.caption(
        "AI Resume Analyzer\n"
        "Built with Python & Streamlit"
    )

st.write("Upload your Resume in PDF format.")

uploaded_file = st.file_uploader(
    "Choose Resume",
    type=["pdf"]
)

# Default values
name = ""
email = ""
phone = ""
linkedin = ""
github = ""
skills = []
education = []
certifications = []
score = 0
suggestions = []
text = ""
missing = []

if "job_analysis" not in st.session_state:
    st.session_state["job_analysis"] = ""


# =====================================================
# START AFTER UPLOAD
# =====================================================

if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully!")

    text = ""

try:

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

except Exception as e:

    st.error("❌ Unable to read this PDF.")
    st.warning(f"Please upload a valid PDF resume.")

    st.stop()
    # =====================================================
    # Resume Text
    # =====================================================

    st.subheader("📄 Extracted Resume")

    st.text_area(
        "Resume Text",
        text,
        height=300
    )

    # =====================================================
    # Extract Resume Details
    # =====================================================

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    github = extract_github(text)

    skills = extract_skills(text)
    education = extract_education(text)
    certifications = extract_certifications(text)

    left, right = st.columns(2)

    with left:

        st.subheader("👤 Candidate Information")

        st.info(
            f"""
**Name:** {name}

**Email:** {email}

**Phone:** {phone}

**LinkedIn:** {linkedin}

**GitHub:** {github}
"""
        )

    with right:

        st.subheader("🛠 Skills")

        if skills:
            for skill in skills:
                st.write("✅", skill)
        else:
            st.write("No Skills Found")

        st.subheader("🎓 Education")

        for edu in education:
            st.write("🎓", edu)

        st.subheader("📜 Certifications")

        for cert in certifications:
            st.write("🏅", cert)


    # =====================================================
    # ATS SCORE
    # =====================================================

    score = calculate_ats_score(
        name,
        email,
        phone,
        linkedin,
        github,
        skills,
        education,
        certifications,
        text
    )

    # Save Resume History
    save_history(
        name,
        email,
        score,
        skills,
        certifications
    )

    st.divider()

    st.subheader("📊 Resume Performance")

    c1, c2, c3 = st.columns(3)

    # ATS Gauge
    with c1:

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "ATS Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 40], "color": "#ff4d4d"},
                        {"range": [40, 70], "color": "#ffd633"},
                        {"range": [70, 100], "color": "#66cc66"},
                    ],
                },
            )
        )

        gauge.update_layout(height=300)

        st.plotly_chart(
            gauge,
            width="stretch"
        )

    # Skills Count
    with c2:
        st.metric(
            "🛠 Skills",
            len(skills)
        )

    # Certificate Count
    with c3:

        if certifications == ["Not Found"]:
            cert_count = 0
        else:
            cert_count = len(certifications)

        st.metric(
            "📜 Certificates",
            cert_count
        )

    st.progress(score / 100)

    if score >= 90:
        st.success("⭐⭐⭐⭐⭐ Excellent Resume!")

    elif score >= 75:
        st.success("👍 Good Resume!")

    elif score >= 60:
        st.warning("⚠ Average Resume. Improve a few sections.")

    else:
        st.error("❌ Resume Needs Improvement.")

    # =====================================================
    # Resume Suggestions
    # =====================================================

    suggestions = get_resume_suggestions(
        email,
        phone,
        linkedin,
        github,
        skills,
        education,
        certifications,
        text
    )

    st.divider()

    st.subheader("💡 Resume Suggestions")

    if suggestions:

        for suggestion in suggestions:
            st.success(suggestion)

    else:

        st.success("🎉 Excellent! Your resume looks well structured.")

    # =====================================================
    # Resume Section Analysis
    # =====================================================

    st.divider()

    st.subheader("📋 Resume Section Analysis")

    sections = analyze_sections(text)

    for section, status in sections.items():

        if "Complete" in status or "Present" in status:
            st.success(f"{section}: {status}")

        else:
            st.error(f"{section}: {status}")


        # =====================================================
    # JOB DESCRIPTION MATCHING
    # =====================================================

    st.divider()

    st.header("🎯 Job Description Matching")

    job_description = st.text_area(
        "Paste the Job Description",
        height=250,
        placeholder="Paste any job description here..."
    )

    if st.button("Analyze Job Match"):

        if job_description.strip() == "":
            st.warning("Please paste a Job Description.")

        else:

            # Match Resume
            match_score, matched, missing = match_resume(
                skills,
                job_description
            )

            st.subheader("🤖 AI Skill Improvement Recommendations")

            if missing:

                with st.spinner("🤖 AI is analyzing your missing skills..."):

                    ai_recommendations = recommend_skill_improvements(
                        missing,
                        job_description
                    )

                st.success("✨ AI analysis completed!")

                st.write(ai_recommendations)

            else:

               st.success(
                "🎉 Excellent! No major missing skills were detected."
               )


            st.subheader("📊 Resume Match Score")

            st.metric(
                "Match Percentage",
                f"{match_score}%"
            )

            st.progress(match_score / 100)

            if match_score >= 80:
                st.success("✅ Excellent Match")

            elif match_score >= 60:
                st.warning("👍 Good Match")

            else:
                st.error("❌ Low Match")

            # =====================================================
            # Pie Chart
            # =====================================================

            fig = px.pie(
                names=["Matched Skills", "Missing Skills"],
                values=[len(matched), len(missing)],
                title="Skill Match Analysis",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

            # =====================================================
            # Matching and Missing Skills
            # =====================================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Matching Skills")

                if matched:
                    for skill in matched:
                        st.success(skill)
                else:
                    st.info("No matching skills found.")

            with col2:

                st.subheader("❌ Missing Skills")

                if missing:
                    for skill in missing:
                        st.error(skill)
                else:
                    st.success("No missing skills detected!")

            # =====================================================
            # Course Recommendation
            # =====================================================

            st.divider()

            st.subheader("📚 Recommended Courses")

            recommendations = recommend_courses(missing)

            if recommendations:

                for course in recommendations:

                    st.success(
                        f"🎯 Skill: {course['Skill']}\n\n"
                        f"📖 Course: {course['Course']}\n\n"
                        f"🏫 Platform: {course['Platform']}"
                    )
            else:

                st.info("No course recommendations available.")

if uploaded_file is not None:

# =====================================================
# 🤖 AI SKILL IMPROVEMENT RECOMMENDATIONS
# =====================================================

 st.divider() 

 st.subheader("🤖 AI Skill Improvement Recommendations")


# =====================================================
# 🎯 AI RESUME VS JOB ANALYSIS
# =====================================================

st.divider()

st.subheader("🎯 AI Resume vs Job Analysis")

if st.button("🤖 Analyze My Resume for This Job"):

    try:

        with st.spinner(
            "🤖 AI is comparing your resume with the job description..."
        ):

            job_analysis = analyze_resume_for_job(
                text,
                job_description,
                missing
            )

        st.session_state["job_analysis"] = job_analysis

        st.success("✨ AI job analysis completed!")

        st.text_area(
            "AI Recommendations",
            job_analysis,
            height=350
        )

        st.download_button(
            label="📥 Download AI Job Analysis",
            data=job_analysis,
            file_name="AI_Job_Analysis.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error("❌ Unable to generate AI job analysis.")

        st.info(
            "Please try again. Make sure your AI service is configured correctly."
        )

        st.session_state["job_analysis"] = ""


# =====================================================
# 📄 PDF REPORT DOWNLOAD
# =====================================================

if uploaded_file is not None:

    st.divider()

    st.subheader("📄 Download Resume Report")

    try:

        generate_report(
            "Resume_Report.pdf",
            name,
            email,
            phone,
            linkedin,
            github,
            skills,
            education,
            certifications,
            score,
            suggestions,
            st.session_state.get("job_analysis", "")
        )

        with open("Resume_Report.pdf", "rb") as pdf_file:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="Resume_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:

        st.error(
            f"Unable to generate PDF report.\n\n{e}"
        )



# =====================================================
# DASHBOARD
# =====================================================

st.divider()

try:

    show_dashboard()

except Exception as e:

    st.warning(
        "Dashboard is unavailable.\n"
        "Check dashboard.py.\n\n"
        f"Error: {e}"
    )


# =====================================================
# END OF RESUME UPLOAD BLOCK
# =====================================================

else:

    st.info("👆 Upload a PDF resume to begin analysis.")
# =====================================================
# 🤖 AI RESUME ASSISTANT
# =====================================================

st.divider()

st.header("🤖 AI Resume Assistant")

st.write(
    "Improve your resume content using AI. "
    "Choose a section, enter your content, and let AI rewrite it "
    "in a professional and ATS-friendly way."
)

# -----------------------------------------------------
# Feature Selection
# -----------------------------------------------------

rewrite_option = st.selectbox(
    "🎯 What do you want to improve?",
    [
        "Professional Summary",
        "Project Description",
        "Work Experience",
        "ATS-Friendly Bullet Points"
    ]
)

# -----------------------------------------------------
# Helpful Description
# -----------------------------------------------------

if rewrite_option == "Professional Summary":

    st.info(
        "💡 Enter your current professional summary. "
        "AI will make it clearer, professional, and ATS-friendly."
    )

elif rewrite_option == "Project Description":

    st.info(
        "💡 Enter your project description. "
        "AI will convert it into strong resume bullet points."
    )

elif rewrite_option == "Work Experience":

    st.info(
        "💡 Enter your work experience. "
        "AI will rewrite it using professional resume language."
    )

else:

    st.info(
        "💡 Enter your resume content. "
        "AI will convert it into ATS-friendly bullet points."
    )

# -----------------------------------------------------
# User Input
# -----------------------------------------------------

resume_content = st.text_area(
    "📝 Enter your content",
    height=200,
    placeholder=(
        "Example:\n"
        "Built a Python project for data analysis..."
    )
)

# -----------------------------------------------------
# AI Button
# -----------------------------------------------------

if st.button(
    "✨ Improve with AI",
    width="stretch"
):

    if resume_content.strip() == "":

        st.warning(
            "⚠️ Please enter some resume content first."
        )

    else:

        with st.spinner(
            "🤖 AI is improving your content..."
        ):

            if rewrite_option == "Professional Summary":

                result = improve_summary(
                    resume_content
                )

            elif rewrite_option == "Project Description":

                result = improve_project(
                    resume_content
                )

            elif rewrite_option == "Work Experience":

                result = improve_experience(
                    resume_content
                )

            else:

                result = generate_bullets(
                    resume_content
                )

        # -------------------------------------------------
        # AI RESULT
        # -------------------------------------------------

        st.success(
            "✨ Your content has been improved!"
        )

        st.subheader(
            "✨ AI-Generated Content"
        )

        st.text_area(
            "Improved Result",
            result,
            height=250
        )

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        st.download_button(
            label="📥 Download Improved Content",
            data=result,
            file_name="Improved_Resume_Content.txt",
            mime="text/plain",
            width="stretch"
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🚀 Developed using Python • Streamlit • PDFPlumber • "
    "Plotly • Scikit-Learn"
)

if uploaded_file is None:

    st.info("👆 Upload a PDF resume to begin analysis.")