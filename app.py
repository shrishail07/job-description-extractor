import streamlit as st
from utils import scrape_job_description, extract_text_from_file, clean_and_parse_jd

st.set_page_config(page_title="Job Description Extractor", layout="wide")

st.title("📄 Job Description Extractor")
st.write("Paste a job description URL or upload a JD file (.pdf, .docx, .txt) to extract structured information.")

url = st.text_input("Enter Job Description URL")

uploaded_file = st.file_uploader("Or upload a JD file", type=["pdf", "docx", "txt"])

if st.button("Extract Job Details"):
    if url:
        with st.spinner("Scraping and processing JD from URL..."):
            jd_text = scrape_job_description(url)
    elif uploaded_file:
        file_bytes = uploaded_file.read()
        with st.spinner("Reading and processing uploaded JD file..."):
            jd_text = extract_text_from_file(file_bytes, uploaded_file.name)
    else:
        st.error("Please provide a job description URL or upload a file.")
        st.stop()

    result = clean_and_parse_jd(jd_text)
    st.subheader("📌 Extracted Job Information")

    for key, value in result.items():
        st.markdown(f"**{key}**: {value if isinstance(value, str) else ', '.join(value)}")

