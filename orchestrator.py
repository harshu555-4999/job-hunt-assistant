import os

from crewai import Crew, Process

from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task


def run_application_crew(job_description, resume_text, llm, api_key=None):
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

    jd_agent = get_jd_analyst_agent(llm)
    resume_agent = get_resume_cl_agent(llm)
    messaging_agent = get_messaging_agent(llm)

    jd_task = create_jd_analysis_task(jd_agent, job_description)
    resume_task = create_resume_cl_task(
        resume_agent,
        "Use the JD Analyst output from the previous task.",
        resume_text,
        context=[jd_task]
    )
    messaging_task = create_messaging_task(
        messaging_agent,
        "Use the JD Analyst output from the previous task.",
        "Use the Resume & Cover Letter Writer output from the previous task.",
        context=[jd_task, resume_task]
    )

    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, messaging_task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff()


if __name__ == "__main__":
    sample_job_description = """
    Software Developer role supporting a federal technology team.
    Responsibilities include Python development, API integration, documentation,
    and collaboration with technical and non-technical stakeholders.
    """

    sample_resume_text = """
    Candidate has experience with Python, APIs, automation, data analysis,
    and building small tools for workflow improvement.
    """

    result = run_application_crew(
        sample_job_description,
        sample_resume_text,
        llm="gemini/gemini-2.0-flash"
    )
    print(result)
