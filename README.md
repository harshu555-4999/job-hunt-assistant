# Job Hunt Assistant

## Live Demo

🚀 https://job-hunt-assistant-bcnkmvx29caus5hsg5gtwf.streamlit.app/

Job Hunt Assistant is a basic learning project that connects USAJobs search, a few CrewAI agents, and a simple Streamlit interface.

The app can:

* Search USAJobs by keyword and location
* Let the user select one job from the results
* Paste resume text
* Run a basic CrewAI workflow
* Generate a job analysis, resume summary, cover letter, outreach message, and follow-up email
* Save the cover letter and log basic application details


Job Hunt Assistant is a basic learning project that connects USAJobs search, a few CrewAI agents, and a simple Streamlit interface.

The app can:

- Search USAJobs by keyword and location
- Let the user select one job from the results
- Paste resume text
- Run a basic CrewAI workflow
- Generate a job analysis, resume summary, cover letter, outreach message, and follow-up email
- Save the cover letter and log basic application details

## Project Structure

- `streamlit_app.py` - Streamlit web interface
- `usajobs_api.py` - Fetches jobs from USAJobs
- `orchestrator.py` - Builds and runs the CrewAI workflow
- `agents/jd_analyst.py` - Job description analysis agent
- `agents/resume_cl_agent.py` - Resume and cover letter agent
- `agents/messaging_agent.py` - Outreach and follow-up message agent
- `utils/config.py` - Loads environment variables
- `utils/tacking.py` - Saves cover letters and logs application details
- `data/` - Output folder for generated files and logs

## Python Version

Use Python 3.11 for this project.

If you have multiple Python versions installed, use the Windows Python launcher:

```powershell
py -3.11 --version
```

## Setup

Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
```

Install the requirements:

```powershell
py -3.11 -m pip install -r requirements.txt
```

Create a `.env` file from `.env.example`:

```powershell
copy .env.example .env
```

Add your USAJobs values:

```env
USAJOBS_API_KEY=your_usajobs_api_key_here
USAJOBS_EMAIL=your_email_used_for_usajobs_here
```

The Gemini API key is entered inside the Streamlit app, so it does not need to be saved in `.env`.

## Running The App

Start Streamlit:

```powershell
py -3.11 -m streamlit run streamlit_app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

If port `8501` is busy, Streamlit may use another port like `8502`.

## Model Options

The sidebar has two model modes.

### Ollama

Use this when you want to run local models and avoid API usage.

Requirements:

- Ollama must be installed
- Ollama must be running
- At least one model should be pulled locally

Useful commands:

```powershell
ollama list
ollama pull qwen3:4b
ollama pull mistral
```

The app reads your local models from `ollama list` and shows them in a dropdown.

### API

Use this when you want to run Gemini through an API key supplied by the user.

Steps:

1. Select `API` in the sidebar.
2. Choose a Gemini model.
3. Paste the user's Gemini API key.
4. Run the workflow.

The key is only entered in the app during the session. It is not written to `.env` by this project.

## Output Files

Generated files are saved under `data/`:

- `data/report.md`
- `data/resume_agent_output.txt`
- `data/messaging_agent_output.txt`
- `data/cover_letters/`
- `data/applications_log.csv`

## Notes

This project is intentionally basic. It is for learning the main flow first: search jobs, select a job, run agents, and save simple outputs.
