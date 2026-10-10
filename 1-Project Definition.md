# Digital Voices of Solidarity

### A Descriptive Analysis of West Bank-Related Posts on X

*Project status: complete. Final deliverable: a 7-tab Streamlit app built from aggregate data only.*

---

## Project Overview

| | |
|:--|:--|
| **Data source** | X (formerly Twitter), public search, no paid API |
| **Collection window** | 14-21 Sep 2026 |
| **Final sample** | 1,058 public posts from accounts with a usable profile location (76 countries) |
| **Unit of analysis** | One post |
| **Country** | Self-reported profile location, geocoded afterward ("profile-based country"). Never geotagging |
| **Deliverables** | 7 notebooks, a Streamlit app, public aggregate files in `data/` |

**Reporting rule used throughout:** never "Country X supports Palestine." Always "posts from accounts with Country X listed as profile location showed...". Results describe the sample, not national populations. Language is descriptive and neutral, with no ranking of countries and no inference about what populations believe.

---

## 1. Research Question

> What does a one-week sample of public X posts mentioning the West Bank look like, and how reliably can expressed support be measured from post text?

---

## 2. Summary of Findings

| Area | Finding (this sample only) |
|:--|:--|
| Size and composition | 1,058 posts from accounts listing 76 countries as profile location. The US accounts for 38.6% (408 posts). Eight countries have 20+ posts and hold 73.3% of the sample |
| Topic | 99.6% of posts contain the phrase "west bank". "Gaza" appears in 38.8% of posts, "palestinian" in 30.3%, "palestine" in 14.9% |
| Time | 93.2% of posts fall on 17-21 Sep, with a peak of 29.3% on 20 Sep |
| Terms | With the search terms hidden, "israeli" (38.1% of posts), "israel" (36.4%) and "occupied" (20.0%) are the most common |
| Co-occurrence | The 20 highest-PMI pairs each rest on 10 to 27 posts; most are names or places, and six come from one news event |
| Hashtags and reach | 11.4% of posts carry a hashtag. The top 1% of posts hold 40.3% of all views |
| Expressed support | Measured on a 100-post hand-labeled pilot (section 6). Support is reported for the pilot only, so no country-level support estimates are made |

---

## 3. Data

### 3.1 Collection

| Item | Detail |
|:--|:--|
| Tool | `twitter-web-exporter` (Tampermonkey userscript) on public X search |
| Query | `(Palestine OR Palestinian OR Gaza OR "West Bank") -filter:replies -filter:retweets` |
| Included | Original posts and quote posts (1,110 of the raw posts were quotes) |
| Excluded | Replies and retweets |
| Raw batch | `batch-3.csv`: 3,326 posts, 1,987 unique authors |

### 3.2 Country Identification

| Location type | Treatment |
|:--|:--|
| Maps reliably to a country (geopy + Nominatim, 83.8% mapped) | Retained |
| Empty | Excluded |
| Vague or junk ("World", "Global") | Excluded |
| Names a place inside the topic itself ("Palestine", "Gaza") | Excluded |
| Cannot be mapped | Excluded |

### 3.3 Filtering Funnel

| Step | Posts left |
|:--|--:|
| Raw posts | 3,326 |
| Phrase filter | 2,830 |
| Author + text de-duplication, cap of 3 posts per author | 2,091 |
| Non-empty profile location | 1,367 |
| Removed topic-named and junk locations | 1,277 |
| Country mapped | 1,070 |
| Repost cluster consolidated (Phase 5) | **1,058** |

### 3.4 Sample Composition

| Country (profile-based) | Posts |
|:--|--:|
| United States | 408 |
| United Kingdom | 147 |
| Canada | 60 |
| Australia | 46 |
| Israel | 38 |
| India | 36 |
| Philippines | 21 |
| Ireland | 20 |
| Other (68 countries) | 282 |

---

## 4. Method by Phase

| Phase | Method | Output |
|:--|:--|:--|
| 1-2. Collection | Public X search through a browser userscript, fixed 14-21 Sep window | `batch-3.csv` (private) |
| 3. Preprocessing | Lowercase, strip URLs, mentions, hashtags and punctuation, remove stopwords, drop tokens of 2 characters or fewer; country mapping | `processed_posts.csv` (private) |
| 4. Term frequencies | Overall and per-country top 20 terms for the 8 countries with 20+ posts | `freq_overall.json`, `freq_by_country.json` |
| 5. Co-occurrence | Same-post co-occurrence, PMI (log base 2), minimum 10 posts per pair | `pmi_results.json` |
| 6. Visualization | Plotly charts in a Streamlit app that reads only aggregate files | Overview, Terms, Co-occurrence, Hashtags, Time tabs |
| 7. Support pilot | Written codebook, random sample of 100 posts hand-labeled from text alone, agreement checks | Sentiment & Support tab |
| 10. Findings | Consolidated results and limitations | Findings tab |

---

## 5. Data Quality Safeguards

| Safeguard | Purpose |
|:--|:--|
| Phrase filter on "west bank" | Removes search matches where the two words appear separately |
| Cap of 3 posts per author, author + text de-duplication | Limits the weight of repeat posters |
| Fixed literal `\n` characters from the JSON export in the tokenizer | Keeps tokens clean |
| Phrase-matched one statement reposted by 13 accounts (kept 1) | Stops a repost cluster from appearing as a word-pair pattern |
| Second term measure: posts containing the term (each term counted once per post) | Prevents one account's repetition from inflating term counts |
| Display filters hide search terms and filler words | Keeps comparisons focused on other vocabulary |
| Each post counts once, with no weighting by views | Avoids letting a few high-reach posts dominate |
| Topic-named and junk locations excluded | Keeps country assignment to real profile locations |
| Labeling sheet with post id and text only; handles and links masked for the second labeler | Keeps labels blind to country and author |
| `files/` is private; the app reads only aggregates in `data/` | No post text or usernames are published |

---

## 6. Validation of the Support Measure

| Check | Result |
|:--|:--|
| Hand labels, 100 random posts | 40 explicit support, 28 no explicit stance, 19 unclear or unrelated, 13 explicit opposition (ranges are wide at n = 100) |
| Same labeler, 40 posts re-labeled | 72% same label, kappa 0.60 (four labels); criticism flag kappa 0.36 |
| Second labeler (Claude, an AI model), same 100 posts | 63% same label on support vs not, kappa 0.11; four labels kappa 0.26; flag kappa 0.28 |
| Keyword baseline for explicit support | Precision 0.14, recall 0.03 |

**Reading:** the difference between labelers appears to come from how posts that criticize Israeli actions, without an explicit statement of support, were treated (unverified). Any "support" figure depends on how support is defined, so support is reported for the pilot only.

---

## 7. Final Outputs

| Output | Where |
|:--|:--|
| Streamlit app (7 tabs: Overview, Terms, Co-occurrence, Hashtags, Time, Sentiment & Support, Findings) | `app.py`, `theme.py`, `sections/` |
| Public aggregates (counts, terms, hashtags, daily counts, PMI, pilot results) | `data/` |
| Notebooks, one per phase | `2-understanding_data.ipynb` to `7-Sentiment & Expressed-Support Analysis.ipynb` |
| Private working files (never published) | `files/` |

---

## 8. What the Data Does Not Allow Us to Conclude

- What any country or population believes.
- A ranking or comparison of countries on support. The support measure was not reliable enough, only the US and UK samples could detect a gap as small as roughly 13 points, date mix differs by country, and posts from one account are not independent.
- Anything about Palestine-related discourse in general, since the sample is posts that mention the West Bank.
- The cause of the date and West Bank skews (unverified).
- Posting activity or trends over time.

---

## 9. Limitations

| # | Limitation | Implication |
|:--:|:--|:--|
| 1 | A sample of public posts, not users or populations | Findings apply to the sample only |
| 2 | Country is self-reported profile location, geocoded and not spot-checked | Some country assignments may be wrong |
| 3 | Sample is 99.6% West Bank-mentioning posts | Not representative of Palestine-related discourse overall |
| 4 | Date skew (93.2% on 17-21 Sep) and different date mixes by country | Daily counts show collection, not activity |
| 5 | Heavy filtering (68.2% excluded) and English-only filtering not fully audited | Possible selection effects |
| 6 | Per-author cap does not limit repetition inside a post; undetected repost clusters may remain | Some counts may be inflated |
| 7 | Single-word tokens; PMI favors names; pairs rest on 10-27 posts; some pairs come from one news event | Pairs are topical bursts, not independent themes |
| 8 | Only 8 of 76 countries have 20+ posts; small countries are sensitive to single viral posts | No reliable country comparison |
| 9 | Views are concentrated; hashtags are sparse; quote posts are included | Reach and hashtags are not used as indicators |
| 10 | Support pilot: n = 100, one human plus one AI labeler, text only, re-label done soon after the first round | Support is reported for the pilot only |
| 11 | X activity does not represent offline opinion | Results should not be generalized beyond the platform |