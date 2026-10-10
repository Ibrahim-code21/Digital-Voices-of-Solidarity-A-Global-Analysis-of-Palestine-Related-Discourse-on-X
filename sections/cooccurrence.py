import json
import math

import plotly.graph_objects as go
import streamlit as st

from theme import DATA, INK, LIGHT, show

# Phase 5 / West Bank check numbers
WB_POSTS, TOTAL_POSTS = 1054, 1058


@st.cache_data
def load_pmi():
    with open(DATA / "pmi_results.json") as f:
        return json.load(f)


def render():
    pairs = sorted(load_pmi(), key=lambda p: p[1])        # lowest first = bottom of chart
    labels = [f"{a} + {b}" for (a, b), _ in pairs]
    scores = [s for _, s in pairs]
    lo, hi = math.floor(min(scores)) - 0.5, max(scores) + 0.3

    st.markdown("#### Word pairs that appear together more than chance")
    with st.expander("How to read this"):
        st.markdown(
            "- A pair counts as appearing together when both words occur in the **same post**.\n"
            "- **PMI** (pointwise mutual information) compares how often two words share a post "
            "with how often they would share one if they were unrelated. Higher means more "
            "surprising, not more frequent.\n"
            "- Only pairs that co-occur in **at least 10 posts** are included, to avoid noise "
            "from rare words."
        )

    fig = go.Figure(
        go.Scatter(
            x=scores, y=labels, mode="markers",
            marker=dict(size=11, color=INK),
            error_x=dict(type="data", symmetric=False, array=[0] * len(scores),
                         arrayminus=[s - lo for s in scores], thickness=1, width=0, color=LIGHT),
            hovertemplate="<b>%{y}</b><br>PMI %{x:.2f}<extra></extra>",
        )
    )
    fig.update_layout(title="Top 20 word pairs by PMI", height=560, showlegend=False,
                      xaxis_title="PMI (higher = appears together more than chance predicts)")
    fig.update_xaxes(range=[lo, hi])
    show(fig)

    st.caption(
        "The axis starts near the lowest score, so dot position, not distance from zero, carries the information. "
        "Most of the highest-scoring pairs are single names or places that tokenization split into words "
        "(for example Ben-Gvir, Strait of Hormuz, Yom Kippur, Saudi Arabia / Riyadh). PMI favors rare, specific "
        "words, so these reflect proper nouns rather than thematic links. One genuinely topical pair is "
        "drones + missiles. A few pairs come from independent posts discussing the same widely shared event. "
        "Twelve verbatim reposts of one statement were removed beforehand; other repost clusters may remain."
    )
    st.markdown(
        f"**Recovering 'West Bank':** single-word counts split it into 'west' and 'bank'. At phrase level, "
        f"{WB_POSTS:,} of {TOTAL_POSTS:,} posts ({WB_POSTS / TOTAL_POSTS:.1%}) contain it."
    )