import streamlit as st
from theme import RAW_POSTS, summary


def render():
    s = summary()
    total, n_eligible = s["total"], s["n_eligible"]
    excluded = 1 - total / RAW_POSTS

    st.subheader("Findings: what this sample shows and what it does not")

    st.markdown(
        "**Short answer to the research question.** This sample cannot show how expressed support for "
        "Palestine varies across countries. Almost every post mentions the West Bank, most countries have too "
        "few posts, and expressed support could not be measured in a way that two labelers agreed on. "
        "What the project does show is what the sample looks like, and how much any measure of support "
        "depends on how support is defined."
    )

    st.markdown("---")
    st.markdown("#### What the sample shows (descriptive, this sample only)")
    st.markdown(
        f"""
- **Size and composition.** {total:,} public posts from accounts listing one of 76 countries as their profile
  location, collected 14-21 Sep 2026 after {excluded:.1%} of {RAW_POSTS:,} raw posts were excluded.
  Accounts listing the US supply 38.6% of posts (408). {n_eligible} countries have 20 or more posts (776 posts, 73.3%).
- **A West Bank sample.** 99.6% of posts contain the phrase "west bank". "Gaza" appears in 38.8% of posts,
  "palestinian" in 30.3% and "palestine" in 14.9%. The same pattern exists in the raw collection (2,824 of 3,326 posts),
  so it comes from how posts were collected, not from later filtering. The exact cause is unverified.
- **Uneven dates.** 93.2% of posts fall on 17-21 Sep, with a peak of 29.3% on 20 Sep. Daily counts show the
  shape of the sample, not posting activity.
- **Terms.** With the search terms hidden, "israeli" (38.1% of posts), "israel" (36.4%) and "occupied" (20.0%)
  are the most common words. Differences between countries' top terms are small and descriptive only.
- **Word pairs.** The 20 highest-PMI pairs each rest on 10 to 27 posts. Most are names or places, and six come from
  one news event (13 posts from 13 accounts). They are topical bursts, not independent themes.
- **Hashtags and reach.** Only 11.4% of posts carry a hashtag (top: westbank 29 posts, palestine 25, israel 24,
  gaza 17). Views are concentrated: the top 1% of posts hold 40.3% of all views. Each post is counted once
  regardless of reach.
"""
    )

    st.markdown("#### Pilot on expressed support (details in the Sentiment & Support tab)")
    st.markdown(
        """
- **100 randomly chosen posts** were hand-labeled from text alone: 40 explicit support, 28 no explicit stance,
  19 unclear or unrelated, 13 explicit opposition. With n = 100 the ranges are wide.
- **Same labeler, 40 posts re-labeled:** 72% same label, kappa 0.60 on four labels and 0.36 on the
  criticism-of-Israeli-actions flag.
- **A second labeler (Claude, an AI model)** applied the written codebook to the same 100 posts: 63% same label on
  support vs not, kappa 0.11. It counted 9 explicit-support posts against 40. The gap appears to come from how posts
  that criticize Israeli actions, without an explicit statement of support, were treated (unverified). Neither
  labeling is treated as correct: the gap shows that any "support" figure depends on its definition.
- **A keyword rule** for explicit support, written before seeing the labels, reached recall 0.03 and precision 0.14
  and was rejected.
"""
    )

    st.markdown("---")
    st.markdown("#### What the data does not allow us to conclude")
    st.markdown(
        """
- **Anything about what a country or population believes.** The only valid wording is "posts from accounts with
  Country X listed as profile location showed...".
- **A ranking or comparison of countries on support.** No test was run. The measure was not reliable, only the US and
  UK samples could detect a gap as small as roughly 13 points (other countries 20 points or more), the date mix differs
  by country (half of Israel-listed posts fall on 20 Sep, half of Ireland-listed posts on 17 Sep), and posts from the
  same account are not independent.
- **Palestine-related discourse in general.** The sample is posts that mention the West Bank.
- **Why the dates and the West Bank mentions are skewed.** The cause is unverified, and no re-collection was done.
- **Posting activity or trends over time.**
- **Planned but not built:** country hypothesis tests and a world map of post counts. Neither would have added
  reliable information to this sample.
"""
    )

    with st.expander("All limitations", expanded=True):
        st.markdown(
            f"""
**Collection and sampling**
- A sample of public posts, not of users or populations. Quote posts are included; replies and retweets are not.
- Public X search with a cap of about 300 results per query (worked around by slicing), occasional rate-limit
  errors, "West Bank" matched as separate words (false positives), and an unreliable language field.
- Posts skew to the West Bank and to 17-21 Sep; cause unverified, no re-collection.

**Processing**
- Country is the self-reported profile location, geocoded afterward (83.8% mapped, not spot-checked).
  Accounts without a usable location were dropped.
- Heavy filtering ({excluded:.1%} excluded) and English-only filtering that was not fully audited.
- A per-author cap of 3 posts limits repeat posters but not repetition inside a post. Undetected repost clusters
  may remain (one was found and removed).

**Analysis**
- Single-word tokens split phrases ("west", "bank"); PMI on single words favors names; scores use log base 2;
  each pair rests on 10 to 27 posts.
- Only {n_eligible} of 76 countries have 20 or more posts; Ireland and the Philippines are indicative only, and
  small countries are sensitive to single viral posts.
- Hashtags are too sparse to use as an indicator; views are highly concentrated.

**Support labeling pilot**
- n = 100, one human labeler and one AI labeler; labels come from text alone, so sarcasm and missing context are
  misread at times. The re-label was done soon after the first round, so agreement may be optimistic.
  The criticism flag is exploratory only.

**Presentation**
- The visual theme is a stylistic choice and carries no analytic meaning.
"""
        )

    st.caption(
        "Suggested description of this project: a descriptive pilot analysis of posts mentioning the West Bank "
        "in a one-week sample of public X posts."
    )