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
# SESSION STATE
# =====================================================

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = None

if "job_analysis" not in st.session_state:
    st.session_state["job_analysis"] = ""

if "job_match_result" not in st.session_state:
    st.session_state["job_match_result"] = None


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
        ],
        key="navigation"
    )

    st.divider()

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


# =====================================================
# HELPER FUNCTION
# =====================================================

def process_resume(uploaded_file):

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for pdf_page in pdf.pages:

            page_text = pdf_page.extract_text()

            if page_text:
                text += page_text + "\n"

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    github = extract_github(text)

    skills = extract_skills(text)
    education = extract_education(text)
    certifications = extract_certifications(text)

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

    sections = analyze_sections(text)

    return {
        "text": text,
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "score": score,
        "suggestions": suggestions,
        "sections": sections
    }


# =====================================================
# 🏠 HOME PAGE
# =====================================================

if page == "🏠 Home":

    st.title("📄 AI Resume Analyzer")

    st.write(
        "Upload your Resume in PDF format to analyze "
        "its ATS score, skills and structure."
    )

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf"],
        key="home_resume_upload"
    )

    if uploaded_file is not None:

        st.success("✅ Resume Uploaded Successfully!")

        # ---------------------------------------------
        # PROCESS RESUME
        # ---------------------------------------------

        try:

            resume_data = process_resume(uploaded_file)

            st.session_state["resume_data"] = resume_data

        except Exception as e:

            st.error(
                "❌ Unable to process the resume."
            )

            st.exception(e)

    resume_data = st.session_state.get("resume_data")

    if resume_data is not None:

        text = resume_data["text"]
        name = resume_data["name"]
        email = resume_data["email"]
        phone = resume_data["phone"]
        linkedin = resume_data["linkedin"]
        github = resume_data["github"]
        skills = resume_data["skills"]
        education = resume_data["education"]
        certifications = resume_data["certifications"]
        score = resume_data["score"]
        suggestions = resume_data["suggestions"]
        sections = resume_data["sections"]

        # ---------------------------------------------
        # SAVE HISTORY
        # ---------------------------------------------

        if (
            "last_saved_resume" not in st.session_state
            or st.session_state["last_saved_resume"] != text
        ):

            try:

                save_history(
                    name,
                    email,
                    score,
                    skills,
                    certifications
                )

                st.session_state["last_saved_resume"] = text

            except Exception:
                pass

        # ---------------------------------------------
        # EXTRACTED RESUME
        # ---------------------------------------------

        st.divider()

        st.subheader("📄 Extracted Resume")

        st.text_area(
            "Resume Text",
            text,
            height=300,
            key="home_resume_text"
        )

        # ---------------------------------------------
        # CANDIDATE INFORMATION
        # ---------------------------------------------

        st.divider()

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

                st.info("No skills found.")

            st.subheader("🎓 Education")

            if education:

                for edu in education:
                    st.write("🎓", edu)

            else:

                st.info("No education found.")

            st.subheader("📜 Certifications")

            if certifications:

                for cert in certifications:
                    st.write("🏅", cert)

            else:

                st.info("No certifications found.")

        # ---------------------------------------------
        # ATS SCORE
        # ---------------------------------------------

        st.divider()

        st.subheader("📊 Resume Performance")

        c1, c2, c3 = st.columns(3)

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
                            {
                                "range": [0, 40],
                                "color": "#ff4d4d"
                            },
                            {
                                "range": [40, 70],
                                "color": "#ffd633"
                            },
                            {
                                "range": [70, 100],
                                "color": "#66cc66"
                            }
                        ]
                    }
                )
            )

            gauge.update_layout(height=300)

            st.plotly_chart(
                gauge,
                width="stretch",
                key="ats_gauge"
            )

        with c2:

            st.metric(
                "🛠 Skills",
                len(skills)
            )

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

            st.success(
                "⭐⭐⭐⭐⭐ Excellent Resume!"
            )

        elif score >= 75:

            st.success(
                "👍 Good Resume!"
            )

        elif score >= 60:

            st.warning(
                "⚠️ Average Resume. "
                "Improve a few sections."
            )

        else:

            st.error(
                "❌ Resume Needs Improvement."
            )

        # ---------------------------------------------
        # RESUME SUGGESTIONS
        # ---------------------------------------------

        st.divider()

        st.subheader("💡 Resume Suggestions")

        if suggestions:

            for suggestion in suggestions:

                st.success(suggestion)

        else:

            st.success(
                "🎉 Excellent! Your resume "
                "looks well structured."
            )

        # ---------------------------------------------
        # SECTION ANALYSIS
        # ---------------------------------------------

        st.divider()

        st.subheader(
            "📋 Resume Section Analysis"
        )

        for section, status in sections.items():

            if (
                "Complete" in status
                or "Present" in status
            ):

                st.success(
                    f"{section}: {status}"
                )

            else:

                st.error(
                    f"{section}: {status}"
                )

        # ---------------------------------------------
        # PDF REPORT
        # ---------------------------------------------

        st.divider()

        st.subheader(
            "📄 Download Resume Report"
        )

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
                st.session_state.get(
                    "job_analysis",
                    ""
                )
            )

            with open(
                "Resume_Report.pdf",
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_file,
                    file_name="Resume_Report.pdf",
                    mime="application/pdf",
                    width="stretch",
                    key="download_pdf_report"
                )

        except Exception as e:

            st.error(
                f"Unable to generate PDF report.\n\n{e}"
            )

    else:

        st.info(
            "👆 Upload a PDF resume to begin analysis."
        )


# =====================================================
# 📊 DASHBOARD PAGE
# =====================================================

elif page == "📊 Dashboard":

    try:

        show_dashboard()

    except Exception as e:

        st.error(
            "❌ Dashboard could not be loaded."
        )

        st.exception(e)


# =====================================================
# 🤖 AI RESUME ASSISTANT
# =====================================================

elif page == "🤖 AI Resume Assistant":

    st.title("🤖 AI Resume Assistant")

    st.write(
        "Improve your resume content and compare "
        "your resume with a job description."
    )

    resume_data = st.session_state.get(
        "resume_data"
    )

    # =================================================
    # JOB DESCRIPTION MATCHING
    # =================================================

    st.divider()

    st.header(
        "🎯 Resume vs Job Description"
    )

    if resume_data is None:

        st.warning(
            "⚠️ Please go to Home and upload "
            "your resume first."
        )

    else:

        text = resume_data["text"]
        skills = resume_data["skills"]

        job_description = st.text_area(
            "Paste the Job Description",
            height=250,
            placeholder=(
                "Paste any job description here..."
            ),
            key="job_description_input"
        )

        if st.button(
            "Analyze Job Match",
            key="analyze_job_match_button",
            width="stretch"
        ):

            if job_description.strip() == "":

                st.warning(
                    "Please paste a Job Description."
                )

            else:

                try:

                    match_score, matched, missing = (
                        match_resume(
                            skills,
                            job_description
                        )
                    )

                    st.session_state[
                        "job_match_result"
                    ] = {
                        "score": match_score,
                        "matched": matched,
                        "missing": missing,
                        "job_description":
                            job_description
                    }

                except Exception as e:

                    st.error(
                        "❌ Unable to analyze job match."
                    )

                    st.exception(e)

        # ---------------------------------------------
        # DISPLAY MATCH RESULT
        # ---------------------------------------------

        job_match = st.session_state.get(
            "job_match_result"
        )

        if job_match is not None:

            match_score = job_match["score"]
            matched = job_match["matched"]
            missing = job_match["missing"]

            st.subheader(
                "📊 Resume Match Score"
            )

            st.metric(
                "Match Percentage",
                f"{match_score}%"
            )

            st.progress(
                match_score / 100
            )

            if match_score >= 80:

                st.success(
                    "✅ Excellent Match"
                )

            elif match_score >= 60:

                st.warning(
                    "👍 Good Match"
                )

            else:

                st.error(
                    "❌ Low Match"
                )

            # -----------------------------------------
            # PIE CHART
            # -----------------------------------------

            fig = px.pie(
                names=[
                    "Matched Skills",
                    "Missing Skills"
                ],
                values=[
                    len(matched),
                    len(missing)
                ],
                title="Skill Match Analysis",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                width="stretch",
                key="job_match_pie"
            )

            # -----------------------------------------
            # MATCHED / MISSING
            # -----------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Matching Skills"
                )

                if matched:

                    for skill in matched:
                        st.success(skill)

                else:

                    st.info(
                        "No matching skills found."
                    )

            with col2:

                st.subheader(
                    "❌ Missing Skills"
                )

                if missing:

                    for skill in missing:
                        st.error(skill)

                else:

                    st.success(
                        "No missing skills detected!"
                    )

            # -----------------------------------------
            # COURSE RECOMMENDATIONS
            # -----------------------------------------

            st.divider()

            st.subheader(
                "📚 Recommended Courses"
            )

            recommendations = (
                recommend_courses(missing)
            )

            if recommendations:

                for course in recommendations:

                    st.success(
                        f"🎯 Skill: {course['Skill']}\n\n"
                        f"📖 Course: {course['Course']}\n\n"
                        f"🏫 Platform: {course['Platform']}"
                    )

            else:

                st.info(
                    "No course recommendations available."
                )

            # -----------------------------------------
            # AI SKILL IMPROVEMENTS
            # -----------------------------------------

            st.divider()

            st.subheader(
                "🤖 AI Skill Improvement Recommendations"
            )

            if missing:

                if st.button(
                    "✨ Generate AI Skill Recommendations",
                    key="ai_skill_recommendation_button",
                    width="stretch"
                ):

                    try:

                        with st.spinner(
                            "🤖 AI is analyzing your missing skills..."
                        ):

                            ai_recommendations = (
                                recommend_skill_improvements(
                                    missing,
                                    job_description
                                )
                            )

                        st.success(
                            "✨ AI analysis completed!"
                        )

                        st.write(
                            ai_recommendations
                        )

                    except Exception as e:

                        st.error(
                            "❌ Unable to generate AI recommendations."
                        )

                        st.exception(e)

            else:

                st.success(
                    "🎉 Excellent! No major missing "
                    "skills were detected."
                )

            # -----------------------------------------
            # AI RESUME VS JOB ANALYSIS
            # -----------------------------------------

            st.divider()

            st.subheader(
                "🎯 AI Resume vs Job Analysis"
            )

            if st.button(
                "🤖 Analyze My Resume for This Job",
                key="ai_job_analysis_button",
                width="stretch"
            ):

                try:

                    with st.spinner(
                        "🤖 AI is comparing your resume "
                        "with the job description..."
                    ):

                        job_analysis = (
                            analyze_resume_for_job(
                                text,
                                job_description,
                                missing
                            )
                        )

                    st.session_state[
                        "job_analysis"
                    ] = job_analysis

                    st.success(
                        "✨ AI job analysis completed!"
                    )

                except Exception as e:

                    st.error(
                        "❌ Unable to generate AI job analysis."
                    )

                    st.info(
                        "Please make sure your AI "
                        "service is configured correctly."
                    )

                    st.session_state[
                        "job_analysis"
                    ] = ""

            if st.session_state.get(
                "job_analysis"
            ):

                st.text_area(
                    "AI Recommendations",
                    st.session_state[
                        "job_analysis"
                    ],
                    height=350,
                    key="ai_recommendations_output"
                )

                st.download_button(
                    label="📥 Download AI Job Analysis",
                    data=st.session_state[
                        "job_analysis"
                    ],
                    file_name="AI_Job_Analysis.txt",
                    mime="text/plain",
                    width="stretch",
                    key="download_ai_analysis"
                )

    # =================================================
    # RESUME REWRITER
    # =================================================

    st.divider()

    st.header(
        "✍️ AI Resume Content Rewriter"
    )

    st.write(
        "Improve your resume content using AI."
    )

    rewrite_option = st.selectbox(
        "🎯 What do you want to improve?",
        [
            "Professional Summary",
            "Project Description",
            "Work Experience",
            "ATS-Friendly Bullet Points"
        ],
        key="rewrite_option"
    )

    if rewrite_option == "Professional Summary":

        st.info(
            "💡 Enter your current professional summary. "
            "AI will make it clearer, professional and ATS-friendly."
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

    resume_content = st.text_area(
        "📝 Enter your content",
        height=200,
        placeholder=(
            "Example:\n"
            "Built a Python project for data analysis..."
        ),
        key="resume_rewriter_input"
    )

    if st.button(
        "✨ Improve with AI",
        width="stretch",
        key="improve_resume_button"
    ):

        if resume_content.strip() == "":

            st.warning(
                "⚠️ Please enter some resume content first."
            )

        else:

            try:

                with st.spinner(
                    "🤖 AI is improving your content..."
                ):

                    if rewrite_option == (
                        "Professional Summary"
                    ):

                        result = improve_summary(
                            resume_content
                        )

                    elif rewrite_option == (
                        "Project Description"
                    ):

                        result = improve_project(
                            resume_content
                        )

                    elif rewrite_option == (
                        "Work Experience"
                    ):

                        result = improve_experience(
                            resume_content
                        )

                    else:

                        result = generate_bullets(
                            resume_content
                        )

                st.success(
                    "✨ Your content has been improved!"
                )

                st.subheader(
                    "✨ AI-Generated Content"
                )

                st.text_area(
                    "Improved Result",
                    result,
                    height=250,
                    key="improved_result"
                )

                st.download_button(
                    label="📥 Download Improved Content",
                    data=result,
                    file_name="Improved_Resume_Content.txt",
                    mime="text/plain",
                    width="stretch",
                    key="download_improved_content"
                )

            except Exception as e:

                st.error(
                    "❌ Unable to improve resume content."
                )

                st.exception(e)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🚀 Developed using Python • Streamlit • "
    "PDFPlumber • Plotly • Scikit-Learn"
)