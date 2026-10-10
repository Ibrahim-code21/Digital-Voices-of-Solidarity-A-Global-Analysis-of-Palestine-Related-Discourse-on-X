import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from theme import INK, MID, load_csv, show


def fmt(d):
    return pd.to_datetime(d).strftime("%d %b")


def daily():
    d = load_csv("posts_per_day.csv")
    total = int(d["posts"].sum())
    d["pct"] = d["posts"] / total * 100
    d["label"] = d["date"].map(fmt)

    first3 = int(d["posts"].iloc[:3].sum())
    peak = d.loc[d["posts"].idxmax()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Share of posts on 17-21 Sep", f"{(total - first3) / total:.1%}")
    c2.metric("Busiest day", f"{peak['label']} ({peak['pct']:.1f}%)")
    c3.metric("Posts on 14-16 Sep combined", f"{first3:,}")

    fig = go.Figure(
        go.Bar(
            x=d["label"], y=d["posts"],
            marker_color=[MID] * 3 + [INK] * (len(d) - 3),
            text=[f"{p:,}" for p in d["posts"]], textposition="outside", cliponaxis=False,
            customdata=d["pct"],
            hovertemplate="<b>%{x}</b><br>%{y:,} posts (%{customdata:.1f}% of sample)<extra></extra>",
        )
    )
    fig.update_layout(title="Posts per day in the sample (UTC)", height=400,
                      yaxis_title="Posts in sample", showlegend=False)
    fig.update_yaxes(range=[0, d["posts"].max() * 1.15])
    show(fig)
    st.caption(
        "Dates are UTC. 14 Sep (from 07:08) and 21 Sep (to 18:47) are partial days. The jump from "
        "16 to 17 Sep is too abrupt to reflect posting activity and most likely comes from how the "
        "sample was collected (X's search cap and the slicing method). These counts show the shape "
        "of the collected sample, not daily posting volumes."
    )


def by_country():
    c = load_csv("country_by_day_pct.csv").sort_values("n_posts", ascending=False)
    date_cols = [x for x in c.columns if x not in ("country", "n_posts")]
    z = c[date_cols].astype(float).values
    ylabels = [f"{r.country} (n={int(r.n_posts)})" for r in c.itertuples()]

    fig = go.Figure(
        go.Heatmap(
            z=z, x=[fmt(x) for x in date_cols], y=ylabels,
            colorscale=[[0, "#FFFFFF"], [1, "#8C8C8C"]], zmin=0, zmax=float(z.max()),
            texttemplate="%{z:.0f}%", textfont=dict(color=INK, size=12),
            hovertemplate="%{y}<br>%{x}: %{z:.0f}% of the country's posts<extra></extra>",
            showscale=False, xgap=2, ygap=2,
        )
    )
    fig.update_layout(title="Share of each country's posts by day (UTC)", height=420)
    fig.update_yaxes(autorange="reversed")
    show(fig)

    notes = []
    for _, r in c.iterrows():
        vals = r[date_cols].astype(float)
        if vals.max() >= 45:
            notes.append(f"{r['country']} ({vals.max():.0f}% on {fmt(vals.idxmax())})")

    st.caption(
        "Each row shows how that country's posts are spread across days (rows sum to about 100%, "
        "allowing for rounding). Posts were not collected evenly across days, so countries differ in "
        "which days they cover. Differences between countries, especially the small ones, partly "
        "reflect which days were captured."
    )
    if notes:
        st.markdown("**Countries with 45% or more of their posts on a single day:** " + "; ".join(notes) + ".")


def render():
    st.markdown("#### Posts per day")
    daily()
    st.markdown("---")
    st.markdown("#### Date mix by country")
    by_country()