import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("AI Resume & Job Matcher")

st.sidebar.header("Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload a PDF/DOCX Resume")

candidate_id = None  # Store candidate ID dynamically

if uploaded_file:
    files = {"resume": uploaded_file}
    response = requests.post(f"{API_BASE}/upload-resume/", files=files)

    try:
        data = response.json()  # Try parsing JSON
        st.sidebar.success("Resume uploaded!")
        
        if "data" in data and "id" in data["data"]:
            candidate_id = data["data"]["id"]  # Store the extracted candidate ID
            st.sidebar.write(f"Candidate ID: {candidate_id}")
        else:
            st.sidebar.error("Candidate ID not found in API response")
        
        st.json(data.get("data", {"message": "No data field in response"}))  # Handle missing data safely
    except requests.exceptions.JSONDecodeError:
        st.error("Error: Received invalid JSON from the API. Check server response.")

st.header("Job Listings")
jobs = requests.get(f"{API_BASE}/upload-job/").json()
st.write("Raw Job Listings Response:", jobs)

for job in jobs:
    st.write(f"**{job['title']}** at {job['company']}")

    if candidate_id: 
        if st.button(f"Match Candidate to {job['title']}", key=f"match_{job['id']}"):
            match = requests.post(f"{API_BASE}/match/", json={"candidate_id": candidate_id, "job_id": job["id"]}).json()
            st.json(match)
    else:
        st.warning("Please upload a resume first.")
