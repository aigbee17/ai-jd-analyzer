import streamlit as st
from analyzer import analyze_job_description, match_resume_to_jd

st.set_page_config(
    page_title="JD Analyzer",
    page_icon="🔍",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .card {
        padding: 1.2rem;
        border-radius: 1rem;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #f3f4f6;
        margin-right: 0.4rem;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Helper Functions ----------
def score_label(score):
    if score >= 80:
        return "Strong"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Review"
    else:
        return "Weak"


def score_emoji(score):
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    elif score >= 40:
        return "🟠"
    else:
        return "🔴"


def show_list(items, empty_message="Nothing found."):
    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.caption(empty_message)


# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ JD Analyzer")
    st.write("Analyze job postings, detect red flags, extract ATS keywords, and compare your resume against the role.")

    st.divider()

    st.markdown("### How to use")
    st.markdown("""
    1. Paste a full job description  
    2. Optional: paste your resume  
    3. Click **Analyze**  
    4. Review scores, skills, and recommendations  
    """)

    st.divider()

    st.markdown("### Best results")
    st.caption("Use the full posting, including responsibilities, qualifications, salary, and company details.")


# ---------- Header ----------
st.markdown('<div class="main-title">🔍 Job Description Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Turn messy job postings into clear insights: skills, red flags, ATS keywords, legitimacy, and resume match.</div>',
    unsafe_allow_html=True
)


# ---------- Inputs ----------
input_col, tip_col = st.columns([2, 1])

with input_col:
    jd_input = st.text_area(
        label="Paste the job description",
        placeholder="Copy and paste the full job posting here...",
        height=280
    )

    resume_input = st.text_area(
        label="Paste your resume, optional",
        placeholder="Paste your resume if you want a match score...",
        height=220
    )

    analyze_btn = st.button("Analyze Job Posting", type="primary", use_container_width=True)

with tip_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ✨ What you’ll get")
    st.markdown("""
    - Legitimacy score  
    - Seniority estimate  
    - Required skills  
    - Nice-to-have skills  
    - ATS keywords  
    - Red flags  
    - Resume match score  
    - Improvement advice  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Pro tip")
    st.caption("If your resume match score is low, check the missing skills and ATS keywords first. Those are usually the fastest fixes.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- Analysis ----------
if analyze_btn:
    if not jd_input.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("Analyzing job description..."):
            result = analyze_job_description(jd_input)

        if "error" in result:
            st.error(result["error"])
        else:
            legitimacy_score = result.get("legitimacy_score", 0)
            legitimacy_status = score_label(legitimacy_score)

            tab1, tab2, tab3 = st.tabs(["📋 Job Breakdown", "🎯 Resume Match", "🧾 Raw JSON"])

            # ---------- Tab 1: Job Breakdown ----------
            with tab1:
                st.markdown("## Job Breakdown")

                top_col1, top_col2, top_col3 = st.columns([2, 1, 1])

                with top_col1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader(result.get("role_title", "Role Title"))
                    st.write(result.get("one_line_summary", "No summary available."))
                    st.markdown(
                        f"""
                        <span class="badge">{result.get("seniority", "Unknown Seniority")}</span>
                        <span class="badge">{legitimacy_status}</span>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                with top_col2:
                    st.metric(
                        label="Legitimacy Score",
                        value=f"{score_emoji(legitimacy_score)} {legitimacy_score}/100"
                    )
                    st.progress(legitimacy_score / 100)

                with top_col3:
                    red_flag_count = len(result.get("red_flags", []))
                    st.metric(label="Red Flags", value=red_flag_count)

                st.divider()

                col_a, col_b = st.columns(2)

                with col_a:
                    with st.expander("🏢 Company Signals", expanded=True):
                        st.write(result.get("company_signals", "—"))

                    with st.expander("✅ Required Skills", expanded=True):
                        show_list(result.get("required_skills", []))

                    with st.expander("⭐ Nice-to-Have Skills", expanded=False):
                        show_list(result.get("nice_to_have_skills", []))

                with col_b:
                    with st.expander("⚠️ Red Flags", expanded=True):
                        red_flags = result.get("red_flags", [])
                        if red_flags:
                            show_list(red_flags)
                        else:
                            st.success("No major red flags detected.")

                    with st.expander("📌 ATS Keywords", expanded=True):
                        keywords = result.get("ats_keywords", [])
                        if keywords:
                            st.write(" · ".join(keywords))
                        else:
                            st.caption("No keywords found.")

                    with st.expander("🧾 Score Reasoning", expanded=False):
                        st.write(result.get("legitimacy_reason", "—"))

            # ---------- Tab 2: Resume Match ----------
            with tab2:
                st.markdown("## Resume Match Analysis")

                if not resume_input.strip():
                    st.info("Paste your resume above and click Analyze to get a match score.")
                else:
                    with st.spinner("Matching your resume to the job..."):
                        match = match_resume_to_jd(jd_input, resume_input)

                    if "error" in match:
                        st.error(match["error"])
                    else:
                        match_score = match.get("match_score", 0)
                        match_status = score_label(match_score)

                        col_score, col_summary = st.columns([1, 3])

                        with col_score:
                            st.metric(
                                label="Match Score",
                                value=f"{score_emoji(match_score)} {match_score}/100"
                            )
                            st.progress(match_score / 100)
                            st.caption(match_status)

                        with col_summary:
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown("### Overall Fit")
                            st.write(match.get("match_summary", "—"))
                            st.markdown('</div>', unsafe_allow_html=True)

                        st.divider()

                        col_m, col_miss, col_irr = st.columns(3)

                        with col_m:
                            st.markdown("### ✅ Matching Skills")
                            show_list(match.get("matching_skills", []))

                        with col_miss:
                            st.markdown("### ❌ Missing Skills")
                            show_list(match.get("missing_skills", []))

                        with col_irr:
                            st.markdown("### ⚪ Less Relevant Skills")
                            show_list(match.get("irrelevant_skills", []))

                        st.divider()

                        col_strong, col_improve = st.columns(2)

                        with col_strong:
                            st.markdown("### 💪 Strong Points")
                            show_list(match.get("strong_points", []))

                        with col_improve:
                            st.markdown("### 🔧 Improvements")
                            show_list(match.get("improvements", []))

            # ---------- Tab 3: Raw JSON ----------
            with tab3:
                st.markdown("## Raw Output")
                st.caption("Useful for debugging or future backend work.")
                st.json(result)

                if resume_input.strip():
                    st.caption("Resume match output appears in the Resume Match tab after analysis.")

st.divider()
st.caption("Built with Streamlit by Ehimenose Aigbe · [GitHub](https://github.com/aigbee17)")