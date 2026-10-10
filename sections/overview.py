import plotly.graph_objects as go
import streamlit as st

from theme import INK, MID, RAW_POSTS, show


def render(s):
    cc, total = s["cc"], s["total"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Posts analysed", f"{total:,}")
    c2.metric("Countries (profile-based)", s["n_eligible"] + s["other_n"])
    c3.metric("Countries with 20+ posts", s["n_eligible"])
    c4.metric("Raw posts retained", f"{total / RAW_POSTS:.1%}")

    d = cc.sort_values("posts")
    fig = go.Figure(
        go.Bar(
            x=d["posts"],
            y=d["country"],
            orientation="h",
            marker_color=[MID if g == "Other" else INK for g in d["group"]],
            text=[f"{p:,} ({pc}%)" for p, pc in zip(d["posts"], d["pct"])],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}: %{x:,} posts<extra></extra>",
        )
    )
    fig.update_layout(title="Posts per profile-based country", height=430,
                      xaxis_title="Posts in sample", showlegend=False)
    fig.update_xaxes(range=[0, d["posts"].max() * 1.22])
    show(fig)
    st.caption(
        f"Eight countries have 20+ posts. The light bar combines the other {s['other_n']} countries. "
        "The United States alone is about 39% of the sample."
    )