import re
import subprocess
from pathlib import Path

import streamlit as st

from usajobs_api import fetch_jobs
from utils.tacking import log_application, save_cover_letter_file


def build_job_description(job):
    return f"""
    Job Title: {job.get("title", "")}
    Agency: {job.get("agency", "")}
    Location: {job.get("location", "")}
    URL: {job.get("url", "")}

    Job Summary:
    {job.get("description", "")}

    Qualifications:
    {job.get("qualifications", "")}
    """


def get_section(text, section_name):
    pattern = rf"<<{section_name}>>(.*?)(?=<<|$)"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def read_output_file(filepath):
    path = Path(filepath)
    if not path.exists():
        return ""
    return path.read_text()


def get_ollama_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
    except Exception:
        return []

    models = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models


st.set_page_config(page_title="Job CHunt Assistant")

st.title("Job Hunt Assistant")
st.write("Search USAJobs, choose one posting, and run the basic CrewAI workflow.")

st.sidebar.header("Model Settings")
model_source = st.sidebar.radio("Model source", ["Ollama", "API"])

api_key = None
if model_source == "API":
    api_provider = st.sidebar.selectbox("API provider", ["Gemini"])
    api_model = st.sidebar.selectbox(
        "API model",
        ["gemini-2.0-flash", "gemini-2.5-flash"]
    )
    api_key = st.sidebar.text_input("Gemini API key", type="password")
    selected_llm = f"gemini/{api_model}"
else:
    ollama_models = get_ollama_models()
    if not ollama_models:
        st.sidebar.warning("No Ollama models found. Make sure Ollama is installed and running.")
        ollama_models = ["qwen3:4b", "qwen2.5:7b", "mistral:latest", "phi3:latest"]
    selected_model = st.sidebar.selectbox("Ollama model", ollama_models)
    selected_llm = f"ollama/{selected_model}"

keyword = st.text_input("Keyword", value="software developer")
location = st.text_input("Location", value="")
results_per_page = st.number_input("Number of jobs", min_value=1, max_value=10, value=5)

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Fetch Jobs"):
    try:
        st.session_state.jobs = fetch_jobs(keyword, location, results_per_page)
        if not st.session_state.jobs:
            st.warning("No jobs found. Try another keyword or location.")
    except Exception as error:
        st.error(f"Could not fetch jobs: {error}")

if st.session_state.jobs:
    job_labels = [
        f"{job['title']} - {job['agency']} - {job['location']}"
        for job in st.session_state.jobs
    ]
    selected_index = st.selectbox(
        "Select a job",
        range(len(job_labels)),
        format_func=lambda index: job_labels[index]
    )
    selected_job = st.session_state.jobs[selected_index]

    st.subheader(selected_job["title"])
    st.write(selected_job["agency"])
    st.write(selected_job["location"])
    if selected_job["url"]:
        st.link_button("Open Job Posting", selected_job["url"])

    resume_text = st.text_area(
        "Paste your resume text",
        height=220,
        placeholder="Paste your resume here before running the workflow."
    )

    if st.button("Run Agent Workflow"):
        if not resume_text.strip():
            st.warning("Please paste your resume text first.")
        elif model_source == "API" and not api_key:
            st.warning("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                from orchestrator import run_application_crew

                with st.spinner("Running the agents..."):
                    result = run_application_crew(
                        build_job_description(selected_job),
                        resume_text,
                        selected_llm,
                        api_key=api_key
                    )
            except ModuleNotFoundError as error:
                st.error(f"Missing package: {error.name}. Run: py -3.11 -m pip install -r requirements.txt")
                st.stop()
            except Exception as error:
                st.error(f"Workflow failed: {error}")
                st.stop()

            output_text = str(result)
            resume_output = read_output_file("data/resume_agent_output.txt")
            messaging_output = read_output_file("data/messaging_agent_output.txt")
            resume_summary = get_section(resume_output, "RESUME_SUMMARY") or output_text[:300]
            cover_letter = get_section(resume_output, "COVER_LETTER")

            if cover_letter:
                save_cover_letter_file(selected_job["title"], cover_letter)
            log_application(selected_job["title"], selected_job["agency"], resume_summary)

            st.success("Workflow finished and application details were logged.")
            st.text_area("Resume and Cover Letter Output", value=resume_output, height=280)
            st.text_area("Messaging Output", value=messaging_output or output_text, height=280)
