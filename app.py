import streamlit as st
import pandas as pd
import plotly.express as px
from data.careers import CAREERS, LEARNING_PATH


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SkillGap - Career Intelligence",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f8f9fc;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    border: 1px solid #eeeeee;
    margin-bottom: 15px;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    text-align: center;
    border: 1px solid #eeeeee;
}

.metric-number {
    font-size: 32px;
    font-weight: bold;
}

.badge {
    padding: 10px 18px;
    border-radius: 20px;
    font-size: 18px;
    font-weight: bold;
    display: inline-block;
}

.small-text {
    color: #666666;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "branch" not in st.session_state:
    st.session_state.branch = ""

if "year" not in st.session_state:
    st.session_state.year = ""

if "career" not in st.session_state:
    st.session_state.career = "Software Developer"

if "skills" not in st.session_state:
    st.session_state.skills = {}

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def calculate_readiness(current_skills, required_skills):
    scores = []

    for skill, required in required_skills.items():
        current = current_skills.get(skill, 0)
        score = min(current / required, 1) * 100
        scores.append(score)

    if scores:
        return round(sum(scores) / len(scores))

    return 0


def get_badge(score):

    if score < 40:
        return "🌱 Beginner", "Start building your foundation."

    elif score < 60:
        return "🚀 Developing", "You are developing useful career skills."

    elif score < 80:
        return "🎯 Job Preparation", "You are getting ready for internships and jobs."

    elif score < 90:
        return "🏆 Career Ready", "You have a strong foundation for your target career."

    else:
        return "🔥 Industry Ready", "Excellent preparation for your target career."


def get_gap_data(current_skills, required_skills):

    data = []

    for skill, required in required_skills.items():

        current = current_skills.get(skill, 0)

        gap = max(required - current, 0)

        if current >= required:
            status = "Strong"
        elif current >= required * 0.7:
            status = "Developing"
        else:
            status = "Needs Improvement"

        data.append({
            "Skill": skill,
            "Current": current,
            "Required": required,
            "Gap": gap,
            "Status": status
        })

    return pd.DataFrame(data)


def get_career_matches(current_skills):

    results = []

    for career, information in CAREERS.items():

        required = information["skills"]

        score = calculate_readiness(
            current_skills,
            required
        )

        results.append({
            "Career": career,
            "Match": score
        })

    results.sort(
        key=lambda x: x["Match"],
        reverse=True
    )

    return results


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎯 SkillGap")

st.sidebar.write(
    "Student Skill & Career Intelligence Platform"
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🧠 Skill Assessment",
        "🎯 Career Match",
        "📊 My SkillGap",
        "🛣️ 90-Day Roadmap",
        "💻 Project Recommendations",
        "🔄 What If?",
        "📄 Career Report"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 SkillGap helps students understand "
    "their current skills, identify gaps and "
    "prepare for their target career."
)


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.markdown("""
    <div class="hero">

    <h1>🎯 SkillGap</h1>

    <p>
    Student Skill & Career Intelligence Platform
    </p>

    <p>
    Discover your career match • Find your skill gaps •
    Build a personalized roadmap
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🚨 The Problem")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">

        ### 🤔 Career Confusion

        Many students are unsure which career
        matches their interests and current skills.

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">

        ### 📉 Unknown Skill Gaps

        Students often don't know which skills
        they need to improve for their dream job.

        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">

        ### 🛣️ No Clear Roadmap

        Students learn random technologies
        without knowing what to learn next.

        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 Our Solution")

    st.write("""
    **SkillGap** analyzes a student's current skills,
    compares them with career requirements and provides
    a personalized career development plan.
    """)

    st.markdown("---")

    st.subheader("✨ What SkillGap Provides")

    features = [
        ("🎯", "Career Matching",
         "Find careers that match your current skills."),

        ("📊", "Skill Gap Analysis",
         "Identify the exact skills you need to improve."),

        ("🧠", "Skill Assessment",
         "Evaluate your technical knowledge."),

        ("🏆", "Readiness Score",
         "Understand how prepared you are."),

        ("🛣️", "90-Day Roadmap",
         "Get a structured learning plan."),

        ("💻", "Project Recommendations",
         "Build projects that improve your weak skills."),

        ("📄", "Career Report",
         "Download your personalized career report.")
    ]

    cols = st.columns(3)

    for index, feature in enumerate(features):

        with cols[index % 3]:

            st.markdown(f"""
            <div class="card">

            <h3>{feature[0]} {feature[1]}</h3>

            <p>{feature[2]}</p>

            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.success(
        "🚀 Start with 'Skill Assessment' from the sidebar!"
    )


# =========================================================
# SKILL ASSESSMENT
# =========================================================

elif page == "🧠 Skill Assessment":

    st.title("🧠 Student Skill Assessment")

    st.write(
        "Enter your profile and rate your current skill level."
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "👤 Student Name",
            value=st.session_state.student_name
        )

        branch = st.selectbox(
            "🎓 Branch",
            [
                "Computer Science Engineering",
                "Information Technology",
                "Artificial Intelligence",
                "Data Science",
                "Electronics",
                "Other"
            ]
        )

    with col2:

        year = st.selectbox(
            "📚 Year",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )

        career = st.selectbox(
            "🎯 Target Career",
            list(CAREERS.keys())
        )

    st.markdown("---")

    st.subheader("📊 Rate Your Skills")

    required_skills = CAREERS[career]["skills"]

    current_skills = {}

    cols = st.columns(2)

    for index, skill in enumerate(required_skills):

        with cols[index % 2]:

            current_skills[skill] = st.slider(
                f"{skill}",
                min_value=0,
                max_value=100,
                value=30,
                step=5
            )

    st.markdown("---")

    if st.button(
        "🚀 Analyze My Skills",
        use_container_width=True
    ):

        score = calculate_readiness(
            current_skills,
            required_skills
        )

        st.session_state.student_name = name
        st.session_state.branch = branch
        st.session_state.year = year
        st.session_state.career = career
        st.session_state.skills = current_skills
        st.session_state.assessment_done = True

        badge, message = get_badge(score)

        st.success("Assessment completed successfully!")

        st.metric(
            "Career Readiness",
            f"{score}%"
        )

        st.markdown(
            f"### {badge}"
        )

        st.write(message)


# =========================================================
# CAREER MATCH
# =========================================================

elif page == "🎯 Career Match":

    st.title("🎯 Career Match Engine")

    st.write(
        "Find which career paths best match your current skills."
    )

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        matches = get_career_matches(
            st.session_state.skills
        )

        st.subheader("🏆 Your Top Career Matches")

        for index, result in enumerate(matches[:3]):

            career_name = result["Career"]
            match_score = result["Match"]

            if index == 0:
                medal = "🥇"
            elif index == 1:
                medal = "🥈"
            else:
                medal = "🥉"

            st.markdown(
                f"### {medal} {career_name}"
            )

            st.progress(
                match_score / 100
            )

            st.write(
                f"**Career Match: {match_score}%**"
            )

            st.markdown("---")

        chart_df = pd.DataFrame(matches)

        fig = px.bar(
            chart_df,
            x="Career",
            y="Match",
            title="Career Compatibility"
        )

        fig.update_yaxes(
            range=[0, 100]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# MY SKILLGAP
# =========================================================

elif page == "📊 My SkillGap":

    st.title("📊 My SkillGap Dashboard")

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        career = st.session_state.career
        current = st.session_state.skills
        required = CAREERS[career]["skills"]

        score = calculate_readiness(
            current,
            required
        )

        badge, message = get_badge(score)

        st.markdown(
            f"## {badge}"
        )

        st.write(message)

        col1, col2, col3, col4 = st.columns(4)

        df = get_gap_data(
            current,
            required
        )

        strong = len(
            df[df["Status"] == "Strong"]
        )

        gaps = len(
            df[df["Gap"] > 0]
        )

        biggest_gap = df.sort_values(
            "Gap",
            ascending=False
        ).iloc[0]

        with col1:
            st.metric(
                "Readiness",
                f"{score}%"
            )

        with col2:
            st.metric(
                "Strong Skills",
                strong
            )

        with col3:
            st.metric(
                "Skills To Improve",
                gaps
            )

        with col4:
            st.metric(
                "Biggest Gap",
                biggest_gap["Skill"]
            )

        st.markdown("---")

        st.subheader(
            f"📈 {career} Skill Analysis"
        )

        chart_data = df[
            ["Skill", "Current", "Required"]
        ].set_index("Skill")

        st.bar_chart(
            chart_data
        )

        st.subheader("🔍 Detailed Skill Gap")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🚨 Top 3 Skills To Improve")

        top_gaps = df.sort_values(
            "Gap",
            ascending=False
        ).head(3)

        for _, row in top_gaps.iterrows():

            st.warning(
                f"**{row['Skill']}** → "
                f"Current: {row['Current']} | "
                f"Required: {row['Required']} | "
                f"Gap: {row['Gap']}"
            )

        st.subheader("💡 Next Best Action")

        skill = biggest_gap["Skill"]

        st.info(
            f"Focus on **{skill}** next. "
            f"{LEARNING_PATH.get(skill, 'Practice this skill through projects and exercises.')}"
        )


# =========================================================
# 90 DAY ROADMAP
# =========================================================

elif page == "🛣️ 90-Day Roadmap":

    st.title("🛣️ Your 90-Day Career Roadmap")

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        career = st.session_state.career

        st.success(
            f"Personalized roadmap for **{career}**"
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "📅 Days 1–30",
                "📅 Days 31–60",
                "📅 Days 61–90"
            ]
        )

        with tab1:

            st.subheader(
                "🌱 Phase 1 — Build Fundamentals"
            )

            st.write("""
            **Week 1–2**
            - Learn the fundamentals of your main programming language.
            - Practice basic syntax.
            - Solve simple coding problems.

            **Week 3–4**
            - Learn important data structures.
            - Practice SQL/database basics.
            - Start using Git and GitHub.
            """)

            st.progress(0.33)

        with tab2:

            st.subheader(
                "🛠️ Phase 2 — Practice & Build"
            )

            st.write("""
            **Week 5–6**
            - Solve intermediate coding problems.
            - Practice your weakest technical skills.

            **Week 7–8**
            - Build a small project.
            - Upload the project to GitHub.
            - Improve your code quality.
            """)

            st.progress(0.66)

        with tab3:

            st.subheader(
                "🚀 Phase 3 — Projects & Job Preparation"
            )

            st.write("""
            **Week 9–10**
            - Build a major portfolio project.
            - Add documentation and screenshots.

            **Week 11**
            - Prepare your resume.
            - Improve LinkedIn and GitHub profiles.

            **Week 12**
            - Practice technical interviews.
            - Apply for internships.
            - Participate in hackathons.
            """)

            st.progress(1.0)

        st.markdown("---")

        st.subheader("📚 Skills To Focus On")

        df = get_gap_data(
            st.session_state.skills,
            CAREERS[career]["skills"]
        )

        top_skills = df.sort_values(
            "Gap",
            ascending=False
        ).head(5)

        for _, row in top_skills.iterrows():

            skill = row["Skill"]

            st.markdown(
                f"### 📌 {skill}"
            )

            st.write(
                LEARNING_PATH.get(
                    skill,
                    "Practice this skill regularly."
                )
            )


# =========================================================
# PROJECT RECOMMENDATIONS
# =========================================================

elif page == "💻 Project Recommendations":

    st.title("💻 Smart Project Recommendation Engine")

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        career = st.session_state.career

        st.success(
            f"Recommended projects for **{career}**"
        )

        df = get_gap_data(
            st.session_state.skills,
            CAREERS[career]["skills"]
        )

        biggest_skills = df.sort_values(
            "Gap",
            ascending=False
        ).head(3)["Skill"].tolist()

        st.subheader("🚨 Build Projects Around Your Skill Gaps")

        for skill in biggest_skills:

            st.markdown(
                f"""
                <div class="card">

                <h3>🎯 Improve {skill}</h3>

                <p>
                Build a project that uses <b>{skill}</b>
                so you improve the skill while creating
                portfolio evidence.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("🔥 Recommended Portfolio Projects")

        projects = CAREERS[career]["projects"]

        for index, project in enumerate(projects, 1):

            st.markdown(
                f"### {index}. 💻 {project}"
            )

            st.write(
                f"This project can help you demonstrate "
                f"skills required for a **{career}** role."
            )

            st.markdown("---")


# =========================================================
# WHAT IF?
# =========================================================

elif page == "🔄 What If?":

    st.title("🔄 What If? Career Comparison")

    st.write(
        "Compare two careers and see which one fits your current skills better."
    )

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        careers = list(CAREERS.keys())

        col1, col2 = st.columns(2)

        with col1:

            career1 = st.selectbox(
                "Career 1",
                careers,
                index=careers.index(
                    st.session_state.career
                )
            )

        with col2:

            career2 = st.selectbox(
                "Career 2",
                careers,
                index=1
            )

        score1 = calculate_readiness(
            st.session_state.skills,
            CAREERS[career1]["skills"]
        )

        score2 = calculate_readiness(
            st.session_state.skills,
            CAREERS[career2]["skills"]
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                f"🎯 {career1}"
            )

            st.metric(
                "Career Match",
                f"{score1}%"
            )

            st.progress(
                score1 / 100
            )

        with col2:

            st.subheader(
                f"🎯 {career2}"
            )

            st.metric(
                "Career Match",
                f"{score2}%"
            )

            st.progress(
                score2 / 100
            )

        if score1 > score2:

            st.success(
                f"🏆 Based on your current skills, "
                f"**{career1}** is currently the stronger match."
            )

        elif score2 > score1:

            st.success(
                f"🏆 Based on your current skills, "
                f"**{career2}** is currently the stronger match."
            )

        else:

            st.info(
                "Both careers currently have the same match score."
            )


# =========================================================
# CAREER REPORT
# =========================================================

elif page == "📄 Career Report":

    st.title("📄 Personalized Career Report")

    if not st.session_state.assessment_done:

        st.warning(
            "⚠️ Complete the Skill Assessment first."
        )

    else:

        name = st.session_state.student_name
        career = st.session_state.career
        score = calculate_readiness(
            st.session_state.skills,
            CAREERS[career]["skills"]
        )

        badge, message = get_badge(score)

        df = get_gap_data(
            st.session_state.skills,
            CAREERS[career]["skills"]
        )

        top_gaps = df.sort_values(
            "Gap",
            ascending=False
        ).head(3)

        report = f"""
SKILLGAP - CAREER INTELLIGENCE REPORT
=====================================

Student Name: {name}
Branch: {st.session_state.branch}
Year: {st.session_state.year}

Target Career:
{career}

Career Readiness:
{score}%

Career Status:
{badge}

{message}

TOP SKILL GAPS
--------------
"""

        for _, row in top_gaps.iterrows():

            report += (
                f"- {row['Skill']}: "
                f"Current {row['Current']} / "
                f"Required {row['Required']}\n"
            )

        report += """

90-DAY ACTION PLAN
------------------

Days 1-30:
Build fundamentals and strengthen weak skills.

Days 31-60:
Practice coding and build projects.

Days 61-90:
Build portfolio projects, improve resume,
practice interviews and apply for internships.

RECOMMENDED PROJECTS
--------------------
"""

        for project in CAREERS[career]["projects"]:

            report += f"- {project}\n"

        report += """

SKILLGAP RECOMMENDATION
-----------------------

Focus first on your biggest skill gaps.
Build practical projects around those skills
and regularly update your GitHub portfolio.

Generated by SkillGap
"""

        st.subheader("👤 Student Profile")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**Name:** {name}")

        with col2:
            st.write(
                f"**Branch:** {st.session_state.branch}"
            )

        with col3:
            st.write(
                f"**Year:** {st.session_state.year}"
            )

        st.markdown("---")

        st.subheader("🏆 Career Result")

        st.metric(
            "Career Readiness",
            f"{score}%"
        )

        st.markdown(
            f"### {badge}"
        )

        st.write(message)

        st.subheader("🚨 Top Skill Gaps")

        for _, row in top_gaps.iterrows():

            st.write(
                f"**{row['Skill']}** — "
                f"{row['Current']} → "
                f"{row['Required']}"
            )

        st.markdown("---")

        st.download_button(
            label="📥 Download Career Report",
            data=report,
            file_name="SkillGap_Career_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.success(
            "Your personalized career report is ready!"
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "🎯 SkillGap | Student Career Intelligence Platform"
)