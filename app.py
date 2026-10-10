import streamlit as st

st.set_page_config(page_title="Digital Voices of Solidarity", layout="wide")

from sections import cooccurrence, findings, hashtags, overview, support, terms, timeline
from theme import RAW_POSTS, inject_css, summary

inject_css()
s = summary()
total, n_eligible = s["total"], s["n_eligible"]

st.title("Digital Voices of Solidarity")
st.markdown('<p class="hero-sub">A Descriptive Analysis of West Bank-Related Posts on X</p>',
            unsafe_allow_html=True)
st.markdown(
    f'<span class="pill">{total:,} public X posts</span>'
    '<span class="pill">14-21 Sep 2026 (UTC)</span>'
    '<span class="pill">Profile-based country</span>'
    '<span class="pill">Support measured on a 100-post pilot only</span>'
    '<span class="pill">Descriptive sample, not national opinion</span>',
    unsafe_allow_html=True,
)

with st.expander("Scope and limitations (read first)", expanded=True):
    st.markdown(
        f"""
- **Sample, not populations.** Results describe a sample of public X posts dated 14-21 Sep 2026.
  They say nothing about what any country or population believes. Country means the
  *profile-based country*: the self-reported profile location of the posting account, geocoded afterward.
- **The sample is almost entirely posts that mention the West Bank** (99.6%).
  Gaza appears in 38.8% of posts and "Palestine" in 14.9%. Results do not cover Palestine-related discourse in general.
- **Dates are uneven.** 93% of posts fall on 17-21 Sep. Daily counts reflect how the sample was collected
  (X's search cap and the slicing method), not daily posting activity. The date mix also differs by country.
- **Heavy filtering.** {RAW_POSTS:,} raw posts became {total:,} ({1 - total / RAW_POSTS:.1%} excluded):
  phrase filter, per-author cap, missing or unmappable locations, and English-only filtering.
  Repeat-post clusters other than the one identified may remain.
- **Small samples.** Only {n_eligible} countries have 20+ posts. Ireland (20) and the Philippines (21)
  are shown for completeness and are indicative only.
- **Expressed support was only piloted** on 100 hand-labeled posts. Labelers did not agree reliably,
  so it was not measured across all posts and countries were not compared (see Findings).
- **Each post counts once** regardless of its reach (views are highly concentrated in a few posts).
"""
    )

tabs = st.tabs(["Overview", "Terms", "Co-occurrence", "Hashtags", "Time",
                "Sentiment & Support", "Findings"])

with tabs[0]:
    overview.render(s)
with tabs[1]:
    terms.render()
with tabs[2]:
    cooccurrence.render()
with tabs[3]:
    hashtags.render()
with tabs[4]:
    timeline.render()
with tabs[5]:
    support.render()
with tabs[6]:
    findings.render()

st.caption("This app shows aggregate counts only. No post text or usernames are published.")