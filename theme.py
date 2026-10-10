import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

DATA = Path(__file__).parent / "data"
RAW_POSTS = 3326  # raw posts collected (batch-3.csv)

INK, MID, LIGHT, GRID = "#222222", "#9A9A9A", "#D9D9D9", "#EBEBEB"
FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"

pio.templates["solidarity"] = go.layout.Template(
    layout=dict(
        font=dict(family=FONT, size=13, color=INK),
        paper_bgcolor="white",
        plot_bgcolor="white",
        colorway=[INK, MID, LIGHT],
        xaxis=dict(gridcolor=GRID, zeroline=False, linecolor=LIGHT),
        yaxis=dict(gridcolor=GRID, zeroline=False, linecolor=LIGHT),
        margin=dict(l=10, r=10, t=55, b=10),
        title=dict(font=dict(size=16)),
    )
)
pio.templates.default = "solidarity"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: Inter, 'Helvetica Neue', Arial, sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1150px; padding-top: 2.2rem; padding-bottom: 3rem; }
h1 { font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.2rem; }
.hero-sub { color: #666; font-size: 1.08rem; margin: 0 0 0.9rem 0; }
.pill { display: inline-block; border: 1px solid #D9D9D9; border-radius: 999px;
        padding: 2px 12px; font-size: 0.8rem; color: #444; margin: 0 6px 6px 0; }
[data-testid="stMetric"] { background: #FAFAFA; border: 1px solid #E5E5E5;
        border-radius: 10px; padding: 14px 16px; }
[data-testid="stMetricValue"] { font-weight: 600; }
[data-testid="stExpander"] { border: 1px solid #E5E5E5; border-radius: 10px; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #E5E5E5; }
.stTabs [data-baseweb="tab"] { font-weight: 500; padding: 8px 14px; }
.soon { border: 1px dashed #D9D9D9; border-radius: 10px; padding: 36px;
        color: #777; text-align: center; margin-top: 1rem; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA / name)


def summary():
    cc = load_csv("country_counts.csv")
    other_label = cc.loc[cc["group"] == "Other", "country"].iloc[0]
    return dict(
        cc=cc,
        total=int(cc["posts"].sum()),
        other_n=int(re.search(r"\((\d+)", other_label).group(1)),
        n_eligible=int((cc["group"] != "Other").sum()),
    )


def show(fig):
    st.plotly_chart(fig, config={"displayModeBar": False})