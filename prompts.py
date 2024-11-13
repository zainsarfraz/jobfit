JOB_DESCRIPTION_ANALYSIS_PROMPT = (
    "You are a helpful assistant, You need to identify the job description and extract the key requirements \
    with the experience. (years in number)\
    Output format should be a table of required (skills \ tech stacks \ key requirements) with its required expereince. \
    Do not give me any other text than the table. \n\
    JOB_DESCRIPTION: {}"
)


EXTRACT_REQUIREMENTS_PROMPT = """You are given a text that can be either a CV text or a job description text, You need 
    If the text is from a job description then identify all of the required skills/tech stacks/requirements from the text along with the 
    experience (in years only integer, overall job years requirement otherwise) required in each. Output format should be a json as [{"skill": skill, "experience": experience_in_years}] \
    If the text is from a CV text then identify all of the skills/tech stacks from the text along with experience
    (in years only integer, overall experience in years otherwise) in each. Output format should be a json as [{"skill": skill, "experience": experience_in_years}] \
    PROVIDE ONLY THE JSON OUTPUT DO NOT GENERATE ANYTHING ELSE """


CV_RATE_PROMPT = """
    You are provided with a comprehensive job description and a user's CV text.
    Your task is to evaluate the compatibility between the user's qualifications and the job requirements.
    Conduct a thorough analysis of the following aspects:

    Skills and Competencies: Assess the user's technical and soft skills relevant to the job description.
    Certifications and Credentials: Identify any certifications or professional accreditations mentioned in the user's CV and determine their relevance to the job.
    Academic Background: Review the user's educational history to see if it aligns with the job's academic requirements.
    Professional Experience: Analyze past job roles, responsibilities, and achievements for alignment with the current job expectations.
    Projects and Contributions: Evaluate any significant projects or contributions that demonstrate the user's expertise related to the job description.
    Based on your evaluation, calculate an overall compatibility score as a percentage and provide a concise summary justifying your assessment.

    Output format: Return the result as a JSON object with the following structure and do not generate anything else or any text other than this json.:

    {
    "percent": <matching percentage>,
    "detail": "<brief justification of your evaluation>"
    }
    Ensure your judgment is objective, comprehensive, and takes into account all aspects of the user's profile compared to the job requirements.
    """
