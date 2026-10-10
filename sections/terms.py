import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from theme import INK, load_csv, show

FILLER = {"one", "also", "would", "even", "still", "said", "like", "may"}


def overall():
    t = load_csv("terms_overall.csv")
    c1, c2, c3 = st.columns([1.3, 1.7, 1])
    measure = c1.radio("Measure", ["Posts containing the term", "Total occurrences"])
    hide_q = c2.checkbox("Hide search terms (west, bank, gaza, palestine, palestinian/s)", value=True)
    hide_f = c2.checkbox("Hide generic filler words", value=True)
    n = c3.slider("Terms shown", 10, 30, 20)

    col = "posts" if measure.startswith("Posts") else "occurrences"
    d = t.copy()
    if hide_q:
        d = d[~d["is_query_term"]]
    if hide_f:
        d = d[~d["term"].isin(FILLER)]
    d = d.sort_values(col, ascending=False).head(n).sort_values(col)

    fig = go.Figure(
        go.Bar(
            x=d[col], y=d["term"], orientation="h", marker_color=INK,
            text=[f"{v:,}" for v in d[col]], textposition="outside", cliponaxis=False,
            customdata=d[["posts", "occurrences", "pct_posts"]].values,
            hovertemplate="<b>%{y}</b><br>%{customdata[0]:,} posts (%{customdata[2]}% of sample)"
                          "<br>%{customdata[1]:,} occurrences<extra></extra>",
        )
    )
    fig.update_layout(title=f"Top {n} terms: {measure.lower()}",
                      height=max(380, 24 * n + 120), showlegend=False)
    fig.update_xaxes(range=[0, d[col].max() * 1.15])
    show(fig)

    if col == "posts":
        st.caption(
            "Each term is counted once per post, so one repetitive post cannot inflate it. "
            "Terms are single words, so 'West Bank' appears as 'west' and 'bank'."
        )
    else:
        st.caption(
            "Occurrences count every use of a word. A few very repetitive posts can inflate them: "
            "in this sample, three posts from one account supply most uses of 'god'. "
            "Compare with the posts view."
        )


def by_country():
    tc = load_csv("terms_by_country.csv")
    order = (tc.drop_duplicates("country")
               .sort_values("n_country_posts", ascending=False)["country"].tolist())
    titles = []
    for c in order:
        n = int(tc.loc[tc["country"] == c, "n_country_posts"].iloc[0])
        titles.append(f"{c} (n={n}{', low volume' if n < 30 else ''})")

    fig = make_subplots(rows=2, cols=4, subplot_titles=titles,
                        horizontal_spacing=0.14, vertical_spacing=0.16)
    for i, c in enumerate(order):
        d = tc[tc["country"] == c].sort_values("pct_posts")
        fig.add_trace(
            go.Bar(
                x=d["pct_posts"], y=d["term"], orientation="h", marker_color=INK,
                customdata=d[["posts", "authors"]].values,
                hovertemplate="<b>%{y}</b><br>%{x:.1f}% of posts"
                              "<br>%{customdata[0]} posts, %{customdata[1]} authors<extra></extra>",
            ),
            row=i // 4 + 1, col=i % 4 + 1,
        )
    fig.update_layout(height=640, showlegend=False,
                      title="Top terms by share of each country's posts (search terms and filler hidden)")
    fig.update_xaxes(range=[0, tc["pct_posts"].max() * 1.1], ticksuffix="%")
    fig.update_yaxes(automargin=True)
    fig.update_annotations(font_size=12)
    show(fig)
    st.caption(
        "Share of that country's posts containing the term. All panels share one scale. "
        "Ireland (n=20) and the Philippines (n=21) are low-volume: one post is about 5%, "
        "and ties are ordered arbitrarily. Hover to see post and author counts. Differences "
        "between countries are descriptive only and mostly small."
    )


def render():
    st.markdown("#### Most frequent terms in the whole sample")
    overall()
    st.markdown("---")
    st.markdown("#### Most frequent terms by country")
    by_country()