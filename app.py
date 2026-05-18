import streamlit as st
from analyzer import analyze_job_description, match_resume_to_jd
 
st.set_page_config(
    page_title="JD Analyzer",
    page_icon="🔍",
    layout="centered"
)
 
st.title("🔍 Job Description Analyzer")
st.caption("Paste any job posting and get an instant AI breakdown — skills, red flags, and a legitimacy score.")
 
# ── Inputs ──────────────────────────────────────────────────────────────
jd_input = st.text_area(
    label="Paste the job description here",
    placeholder="Copy and paste the full job posting...",
    height=250
)
 
resume_input = st.text_area(
    label="Paste your resume here (optional — for match analysis)",
    placeholder="Copy and paste your resume as plain text...",
    height=250
)
 
analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
 
# ── Analysis ─────────────────────────────────────────────────────────────
if analyze_btn:
    if not jd_input.strip():
        st.warning("Please paste a job description first.")
    else:
 
        # ── JD Analysis ──
        with st.spinner("Analyzing job description..."):
            result = analyze_job_description(jd_input)
 
        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("📋 Job Breakdown")
 
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(result.get("role_title", "Role"))
                st.caption(result.get("one_line_summary", ""))
            with col2:
                score = result.get("legitimacy_score", 0)
                color = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                st.metric(label="Legitimacy", value=f"{color} {score}/100")
 
            st.divider()
 
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Seniority**")
                st.write(result.get("seniority", "—"))
            with col_b:
                st.markdown("**Company signals**")
                st.write(result.get("company_signals", "—"))
 
            st.divider()
 
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
 
            st.markdown("**ATS keywords to include on your resume**")
            keywords = result.get("ats_keywords", [])
            st.write("  ·  ".join(keywords))
 
            st.divider()
 
            red_flags = result.get("red_flags", [])
            if red_flags:
                st.markdown("**⚠️ Red flags**")
                for flag in red_flags:
                    st.markdown(f"- {flag}")
            else:
                st.success("No major red flags detected.")
 
            st.caption(f"Legitimacy score reasoning: {result.get('legitimacy_reason', '')}")
 
        # ── Resume Match Analysis ──
        if resume_input.strip():
            st.divider()
            st.subheader("🎯 Resume Match Analysis")
 
            with st.spinner("Matching your resume to the job..."):
                match = match_resume_to_jd(jd_input, resume_input)
 
            if "error" in match:
                st.error(match["error"])
            else:
                # Match score hero metric
                match_score = match.get("match_score", 0)
                match_color = "🟢" if match_score >= 70 else "🟡" if match_score >= 50 else "🔴"
 
                col_score, col_summary = st.columns([1, 3])
                with col_score:
                    st.metric(label="Match Score", value=f"{match_color} {match_score}/100")
                with col_summary:
                    st.markdown("**Overall fit**")
                    st.write(match.get("match_summary", "—"))
 
                st.divider()
 
                # Three skill columns
                col_m, col_miss, col_irr = st.columns(3)
                with col_m:
                    st.markdown("**✅ Matching skills**")
                    for skill in match.get("matching_skills", []):
                        st.markdown(f"- {skill}")
                with col_miss:
                    st.markdown("**❌ Missing skills**")
                    for skill in match.get("missing_skills", []):
                        st.markdown(f"- {skill}")
                with col_irr:
                    st.markdown("**⚪ Irrelevant skills**")
                    for skill in match.get("irrelevant_skills", []):
                        st.markdown(f"- {skill}")
 
                st.divider()
 
                col_strong, col_improve = st.columns(2)
                with col_strong:
                    st.markdown("**💪 Strong points**")
                    for point in match.get("strong_points", []):
                        st.markdown(f"- {point}")
                with col_improve:
                    st.markdown("**🔧 Improvements**")
                    for tip in match.get("improvements", []):
                        st.markdown(f"- {tip}")
 
st.divider()
st.caption("Built with Streamlit by Ehimenose Aigbe · [GitHub](https://github.com/aigbee17)")