import plotly.graph_objects as go
import streamlit as st

from theme import INK, MID, load_csv, show

DISTINCT_TAGS = 292  # distinct hashtags across the sample (Phase 6, Step 5)


def render():
    ht = load_csv("hashtags_overall.csv")
    total = int(ht["n_posts_total"].iloc[0])
    tagged = int(ht["n_posts_with_tag"].iloc[0])

    c1, c2, c3 = st.columns(3)
    c1.metric("Posts with at least one hashtag", f"{tagged:,}")
    c2.metric("Share of all posts", f"{tagged / total:.1%}")
    c3.metric("Distinct hashtags", DISTINCT_TAGS)

    st.markdown("#### Most used hashtags")
    a, b = st.columns([1, 2])
    n = a.slider("Hashtags shown", 8, 25, 15)
    min3 = b.checkbox("Only hashtags used by 3 or more different authors", value=False)

    ranked = ht.sort_values(["posts", "authors"], ascending=False)
    after_top4 = int(ranked["posts"].iloc[4])

    d = ranked[ranked["authors"] >= 3] if min3 else ranked
    d = d.head(n).sort_values("posts")

    fig = go.Figure(
        go.Bar(
            x=d["posts"],
            y=["#" + h for h in d["hashtag"]],
            orientation="h",
            marker_color=[MID if q else INK for q in d["is_query_tag"]],
            text=[f"{x} authors" for x in d["authors"]],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x} posts, %{text}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Top {len(d)} hashtags by number of posts",
        height=max(360, 26 * len(d) + 120),
        xaxis_title="Posts containing the hashtag",
        showlegend=False,
    )
    fig.update_xaxes(range=[0, d["posts"].max() * 1.2])
    show(fig)

    st.caption(
        "Light bars are tags that mirror the search terms (#westbank, #palestine, #gaza). "
        "Hashtags are matched case-insensitively. The label on each bar is the number of different "
        "authors who used the tag: where posts clearly exceed authors, one account repeated it."
    )
    st.markdown(
        f"**Coverage and limits.** Only {tagged / total:.1%} of posts carry any hashtag, so these counts "
        f"describe a small slice of the sample. Beyond the four most common tags, none appears in more than "
        f"{after_top4} posts ({after_top4 / total:.1%} of the sample). For that reason hashtags are not used "
        "as an indicator of expressed support in this project, and they are not broken down by country."
    )