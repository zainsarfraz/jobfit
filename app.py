import streamlit as st
from controller import analyze_cv, clear_text, analyze_job_description


st.title("JobFit")
alert_placeholder = st.empty()
cv_file = st.file_uploader("Upload CV File", type=["pdf"])
job_description = st.text_area("Enter Job Description:")
col1, col2, col3 = st.columns(3, gap="large")
spinner_placeholder = st.empty()
percent_chart_placeholder = st.empty()
output_text = st.empty()

with col1:
    if st.button(
        label="Analyze Job",
        use_container_width=True,
        icon=":material/query_stats:",
        type="primary",
    ):
        analyze_job_description(job_description, spinner_placeholder, alert_placeholder)
with col2:
    if st.button(
        label="Analyze CV",
        use_container_width=True,
        icon=":material/person_check:",
        type="primary",
    ):
        analyze_cv(cv_file, job_description, spinner_placeholder, alert_placeholder)
with col3:
    if st.button(
        label="Clear",
        use_container_width=True,
        icon=":material/delete_forever:",
    ):
        clear_text()


if (
    "percent_chart" in st.session_state
    and st.session_state["percent_chart"] is not None
):
    percent_chart_placeholder.plotly_chart(st.session_state["percent_chart"])

if "output_text" in st.session_state:
    output_text.markdown(st.session_state["output_text"])
