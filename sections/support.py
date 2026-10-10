import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from theme import INK, MID, LIGHT, GRID, load_csv, show
_csv = load_csv

@st.cache_data
def _csv(name):
    return pd.read_csv(f"data/{name}")

def render():
    st.subheader("Sentiment & Support: pilot on a hand-labeled sample")
    st.markdown(
        "A random sample of **100 posts** was hand-labeled from text alone, using a written codebook. "
        "Labels describe posts in this sample, not countries or populations. "
        "Bars show shares with 95% ranges; with n=100 the ranges are wide."
    )

    c = _csv("stance_pilot_counts.csv")
    fig = go.Figure(go.Bar(
        x=c["pct"], y=c["label"], orientation="h", marker_color=INK,
        error_x=dict(type="data", symmetric=False,
                     array=c["ci_high"] - c["pct"], arrayminus=c["pct"] - c["ci_low"], color=MID),
        text=[f"{p:.0f}% (n={n})" for p, n in zip(c["pct"], c["posts"])],
        textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(
        height=300, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(color=INK), margin=dict(l=10, r=60, t=10, b=10),
        xaxis=dict(title="% of labeled posts", range=[0, 100], gridcolor=GRID, zeroline=False),
        yaxis=dict(autorange="reversed"),
    )
    show(fig)

