import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Recruiter Analytics Dashboard")

if "results" not in st.session_state:

    st.warning(
        "Please analyze resumes first."
    )

else:

    results = st.session_state["results"]

    total_candidates = len(results)

    avg_score = round(
        sum(
            c["ats_score"]
            for c in results
        ) / total_candidates,
        2
    )

    top_candidate = results[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Candidates",
        total_candidates
    )

    col2.metric(
        "Average ATS Score",
        f"{avg_score}%"
    )

    col3.metric(
        "Top Candidate",
        top_candidate["candidate"]
    )

    st.markdown("---")

    chart_df = pd.DataFrame({

        "Candidate": [
            c["candidate"]
            for c in results
        ],

        "ATS Score": [
            c["ats_score"]
            for c in results
        ]
    })

    fig = px.bar(
        chart_df,
        x="Candidate",
        y="ATS Score",
        text="ATS Score",
        title="Candidate Score Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )