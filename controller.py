import streamlit as st
from pypdf import PdfReader
from prompts import JOB_DESCRIPTION_ANALYSIS_PROMPT, CV_RATE_PROMPT
from groq_service import stream_groq_chat
from plotly_service import cv_percent_graph
import json
import logging

logging.basicConfig(level=logging.INFO)


def extract_skills_and_experiences(data):
    skills = [entry["skill"] for entry in data]
    experiences = [entry["experience"] for entry in data]
    return skills, experiences


def clear_text():
    st.session_state["output_text"] = ""
    st.session_state["percent_chart"] = None


def analyze_cv(cv_file, job_description, spinner_placeholder, alert_placeholder):
    clear_text()

    if cv_file is None:
        alert_placeholder.error("Please upload your CV")
        return

    if not job_description:
        alert_placeholder.error("Please enter Job description")
        return

    pdf_reader = PdfReader(cv_file)
    cv_text = ""
    for page in pdf_reader.pages:
        cv_text += page.extract_text() + "\n"

    with spinner_placeholder.container():
        with st.spinner("Processing..."):
            chat = [
                {"role": "system", "content": CV_RATE_PROMPT},
                {
                    "role": "user",
                    "content": f"CV text: {cv_text},\n Job Description: {job_description}",
                },
            ]

            output = ""
            for chunk in stream_groq_chat(chat=chat, temprature=0.4):
                output += chunk

            logging.info(f"output {output}")
            try:
                json_output = json.loads(output)
            except Exception as e:
                logging.error(e)
                alert_placeholder.error("Failed to evaluate, Try again later.")
                return

            fig = cv_percent_graph(int(json_output["percent"]))

            st.session_state["percent_chart"] = fig
            st.session_state["output_text"] = json_output["detail"]


def analyze_job_description(job_description, spinner_placeholder, alert_placeholder):
    clear_text()

    if not job_description:
        alert_placeholder.error("Please enter Job description")
        return

    with spinner_placeholder.container():
        with st.spinner("Processing..."):
            chat = [
                {"role": "system", "content": JOB_DESCRIPTION_ANALYSIS_PROMPT},
                {"role": "user", "content": job_description},
            ]

            for chunk in stream_groq_chat(chat=chat):
                st.session_state["output_text"] += chunk
