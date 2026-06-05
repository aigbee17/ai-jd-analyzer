# 🎯 JD Analyzer - Job Description Intelligence Tool

**Turn messy job postings into clear insights: skills, red flags, ATS keywords, legitimacy, and resume match.**

![JD Analyzer Interface](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-98.2%25-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

JD Analyzer is an intelligent job description analysis tool powered by AI that helps job seekers make informed decisions. Paste any job posting and get comprehensive insights including:

### 📊 What You'll Get
- **Legitimacy Score** - Assess how genuine the job posting is
- **Seniority Estimate** - Understand the actual experience level required
- **Required Skills** - Extract and categorize essential skills
- **Nice-to-Have Skills** - Identify beneficial but optional qualifications
- **ATS Keywords** - Discover keywords optimized for Applicant Tracking Systems
- **Red Flags** - Identify potential issues or concerns in the posting
- **Resume Match Score** - Compare your resume against the job requirements
- **Improvement Advice** - Get actionable recommendations to strengthen your candidacy

## 🚀 Features

### Core Capabilities
- **Job Breakdown Analysis** - Comprehensive dissection of job descriptions
- **Resume Comparison** - Optional resume upload for match scoring
- **Multi-Tab Results** - View analysis through different lenses:
  - Job Breakdown (detailed analysis)
  - Resume Match (compatibility scoring)
  - Raw JSON (technical output)
- **Company Intelligence** - Detect company signals and verify legitimacy
- **Skill Extraction** - AI-powered extraction of technical and soft skills
- **Red Flag Detection** - Identify suspicious or unrealistic requirements

### Best Practices
For best results:
- Use the full posting, including responsibilities, qualifications, salary, and company details
- Include company information for legitimacy assessment
- Optionally provide your resume for accurate match scoring
- If your resume match score is low, focus on missing skills and ATS keywords first

## 💻 Tech Stack

- **Backend**: Python
- **Deployment**: Docker, Google Cloud Run
- **AI/ML**: LLM-powered analysis
- **Frontend**: Streamlit
- **Infrastructure**: Cloud-native, serverless

## 📖 How to Use

### Step-by-Step Guide

1. **Paste Job Description**
   - Copy and paste the full job posting into the main text area
   - Include all relevant details: role, company, responsibilities, qualifications

2. **Optional: Add Resume**
   - Paste your resume if you want a match score
   - This enables resume comparison and compatibility analysis

3. **Click Analyze**
   - Press the "Analyze Job Posting" button
   - Wait for AI processing (typically 5-30 seconds)

4. **Review Results**
   - **Job Breakdown Tab**: Explore detailed analysis including skills, red flags, and company signals
   - **Resume Match Tab**: See how well your background aligns with requirements
   - **Raw JSON Tab**: Access structured technical data

### Pro Tips
- 💡 If your resume match score is low, focus on updating your experience with ATS keywords first
- 💡 Red flags often relate to missing skills or team structure information
- 💡 A legitimate score isn't definitive—use it as one factor among many
- 💡 High legitimacy jobs typically have clear company info, detailed responsibilities, and realistic salary ranges

## 🏗️ Deployment

### Prerequisites
- Google Cloud Account with billing enabled
- `gcloud` CLI installed and configured
- Docker installed (for local testing)

**Happy job hunting! 🚀 Use JD Analyzer to make smarter career decisions.**

**Last Updated**: June 2026  
**Version**: 1.0.0
