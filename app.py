import streamlit as st
from src.helper import extract_text_from_pdf, ask_model
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="Job Recommendation System", page_icon=":briefcase:", layout="wide")
st.title("AI Job Recommender")
st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri.com.")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        
    with st.spinner("Summarizing your resume..."):
        summary = ask_model(f"Summarize this resume highlighting the skills, education and expeience: \n\n{resume_text}", max_tokens=500)
        
    with st.spinner("Finding skill gaps..."):
        gaps = ask_model(f"Analyze the attached resume and provide a detailed evaluation of its strengths and weaknesses. Highlight any missing technical or soft skills, certifications, projects, and professional experiences that could enhance the candidate’s chances of securing better job opportunities in their target field. Also, suggest specific improvements to the formatting, structure, and content to make it more impactful and ATS-friendly. Here is the resume: \n\n{resume_text}", max_tokens=500)
        
    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_model(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certifications required and industry exposere): \n\n{resume_text}", max_tokens=400)
        
        
    # Display nicely formatted results
    # Resume Summary
    st.markdown("---")
    st.header("Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    # Skill Gaps
    st.markdown("---")
    st.header("Skill Gaps & Improvement Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    # Career Roadmap
    st.markdown("---")
    st.header("Career Roadmap")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    
    st.success("Analysis Complete Successfully!")
    
    if st.button("Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keyword = ask_model(
                f"Based on this resume summary, suggest the best job titles and keywords for searching relevant jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}", 
                max_tokens=100
                )
            
            search_keywords_clean= keyword.replace("\n", "").strip()
            
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")
        
        with st.spinner("Fetching LinkedIn and Naukri jobs..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=50)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=50)
            
            st.markdown("---")
            st.header(" Top Naukri.com Jobs")
            
            if naukri_jobs:
                for job in naukri_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"Location: {job.get('location')}")
                    st.markdown(f"[Apply Here]({job.get('url')})")
                    st.markdown("---")
            else:
                st.warning("No Naukri.com jobs found.")
            
            st.markdown("---")
            st.header(" Top LinkedIn Jobs")
            
            if linkedin_jobs:
                for job in linkedin_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"Location: {job.get('location')}")
                    st.markdown(f"[Apply Here]({job.get('url')})")
                    st.markdown("---")
            else:
                st.warning("No LinkedIn jobs found.")
                
            