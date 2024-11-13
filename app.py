import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompts import JOB_DESCRIPTION_ANALYSIS_PROMPT, EXTRACT_REQUIREMENTS_PROMPT, CV_RATE_PROMPT
import logging
import os
from pypdf import PdfReader
import json
import plotly.graph_objects as go
from utils import extract_skills_and_experiences


load_dotenv()
client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
logging.basicConfig(level=logging.INFO)

if 'output_text' not in st.session_state:
    st.session_state['output_text'] = ""

st.title('JobFit')
cv_file = st.file_uploader("Upload CV File", type=["pdf"])
job_description = st.text_area("Enter Job Description:")
col1, col2, col3 = st.columns(3, gap="large")
spinner_placeholder = st.empty()


def analyze_job_description():
    clear_text()
    if not job_description:
        st.error("Please enter Job description")
        return
    with spinner_placeholder.container():
        with st.spinner("Processing..."):
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": JOB_DESCRIPTION_ANALYSIS_PROMPT},
                    {"role": "user", "content": job_description}
                ],
                model="llama-3.2-90b-vision-preview",
                stream=True
            )
                            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    st.session_state['output_text'] += str(chunk.choices[0].delta.content)

def clear_text():
    st.session_state['output_text'] = ""
    st.session_state['spider_plot'] = None
    output_text.empty()


def analyze_cv():
    clear_text()
    if cv_file is None:
        st.error("Please upload your CV")
        return
    if not job_description:
        st.error("Please enter job description")
        return

    pdf_reader = PdfReader(cv_file)
    cv_text = ""
    for page in pdf_reader.pages:
        cv_text += page.extract_text() + "\n"
    
    with spinner_placeholder.container():
        with st.spinner("Processing..."):
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": CV_RATE_PROMPT},
                    {"role": "user", "content": f"CV text: {cv_text},\n Job Description: {job_description}"}
                ],
                model="llama-3.2-90b-vision-preview",
                stream=True,
                temperature=0.4
            )

            output = ""     
            for chunk in response:
                if chunk.choices[0].delta.content:
                    output += str(chunk.choices[0].delta.content)

            logging.info(f"output {output}")
            json_output = json.loads(output)

            fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=int(json_output['percent']),
                    title={'text': "CV Match %"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#63f542"},
                        'steps': [
                            {'range': [0, 50], 'color': "#f56342"},
                            {'range': [50, 75], 'color': "#ecf542"},
                            {'range': [75, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': int(json_output['percent'])
                        }
                    }
                ))

            st.session_state['spider_plot'] = fig
            st.session_state['output_text'] = json_output['detail']

if 'spider_plot' in st.session_state and st.session_state['spider_plot'] is not None:
    st.plotly_chart(st.session_state['spider_plot'])

output_text = st.empty()
output_text.markdown(st.session_state['output_text'])

with col1:
    st.button(label="Analyze Job", use_container_width=True, icon=":material/query_stats:", on_click=analyze_job_description, type="primary")
with col2:
    st.button(label="Analyze CV", use_container_width=True, icon=":material/person_check:", on_click=analyze_cv, type="primary")
with col3:
    st.button(label="Clear", use_container_width=True, icon=":material/delete_forever:", on_click=clear_text)
