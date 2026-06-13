from crewai import Agent, Task

def get_messaging_agent(llm):
    return Agent(
        role="Application Messaging Assistant",
        goal="Create simple professional messages for job applications",
        backstory="You're good at writing short, polite messages for recruiters, hiring managers, and follow-ups.",
        llm=llm,
        verbose=True
    )

def create_messaging_task(agent, job_summary, resume_cover_letter, context=None):
    return Task(
        description=f"""
        Based on the job summary and application material below, write simple professional messages the candidate can use.

        --- Job Summary ---
        {job_summary}

        --- Resume and Cover Letter Draft ---
        {resume_cover_letter}

        Your output should include:
        1. A short LinkedIn/recruiter outreach message
        2. A brief follow-up email after applying
        """,
        agent=agent,
        expected_output="""
        <<OUTREACH_MESSAGE>>
        [Short professional outreach message here]

        <<FOLLOW_UP_EMAIL>>
        [Brief follow-up email here]
        """,
        context=context or [],
        output_file='data/messaging_agent_output.txt'
    )
