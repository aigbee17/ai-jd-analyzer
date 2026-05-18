import streamlit as st
from analyzer import analyze_job_description

st.set_page_config(
    page_title="JD Analyzer",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Job Description Analyzer")
st.caption("Paste any job posting and get an instant AI breakdown — skills, red flags, and a legitimacy score.")

jd_input = st.text_area(
    label="Paste the job description here",
    placeholder="Copy and paste the full job posting...",
    height=280
)

analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

if analyze_btn:
    if not jd_input.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_job_description(jd_input)

        if "error" in result:
            st.error(result["error"])
        else:
            # Header row
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(result.get("role_title", "Role"))
                st.caption(result.get("one_line_summary", ""))
            with col2:
                score = result.get("legitimacy_score", 0)
                color = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                st.metric(label="Legitimacy", value=f"{color} {score}/100")

            st.divider()

            # Seniority + company signals
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Seniority**")
                st.write(result.get("seniority", "—"))
            with col_b:
                st.markdown("**Company signals**")
                st.write(result.get("company_signals", "—"))

            st.divider()

            # Skills columns
            col_req, col_nice = st.columns(2)
            with col_req:
                st.markdown("**Required skills**")
                for skill in result.get("required_skills", []):
                    st.markdown(f"- {skill}")
            with col_nice:
                st.markdown("**Nice to have**")
                for skill in result.get("nice_to_have_skills", []):
                    st.markdown(f"- {skill}")

            st.divider()

            # ATS keywords
            st.markdown("**ATS keywords to include on your resume**")
            keywords = result.get("ats_keywords", [])
            st.write("  ·  ".join(keywords))

            st.divider()

            # Red flags
            red_flags = result.get("red_flags", [])
            if red_flags:
                st.markdown("**⚠️ Red flags**")
                for flag in red_flags:
                    st.markdown(f"- {flag}")
            else:
                st.success("No major red flags detected.")

            # Legitimacy reasoning
            st.caption(f"Legitimacy score reasoning: {result.get('legitimacy_reason', '')}")

st.divider()
st.caption("Built with Streamlit by Ehimenose Aigbe · [GitHub](https://github.com/aigbee17)")