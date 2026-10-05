---
name: seo-outline
description: Build an SEO/GEO article outline (Title + H2/H3) from a main keyword and sub keywords, based on real research of top-ranking pages, sub keyword intent analysis, and a title that contains the main keyword. Use when the user gives a main keyword / sub keyword and asks for an outline ("làm outline", "tạo outline", "lên dàn ý", "outline cho keyword").
---

# SEO Outline Builder

Turn a main keyword + sub keywords into a researched outline the user can hand to the `seo-article` skill.

## 0. Inputs

- **Main keyword**: required. Ask if missing.
- **Sub keyword(s)**: optional, may be several.

## 1. Research first (mandatory, real, not from memory)

Never draft any heading or title before this step is done. Do not outline from memory or from the example in this file. If WebSearch/WebFetch fail, tell the user and stop instead of guessing.

1. WebSearch the main keyword. Note which pages rank at the top and what type they are (how-to guide, listicle, comparison, local list, official support page, forum).
2. WebFetch the full content (not just snippets) of at least 1 to 3 of the most authoritative ranking pages. Extract their real H2/H3 structure.
3. Note what they all cover (must-have sections), what they miss (gaps), and the dominant format.
4. Flag anything important the reader must know before the outline:
   - surprising facts, common misconceptions,
   - conflicting expert opinions,
   - safety warnings.
5. Health topics: prioritise medical accuracy (official health bodies, peer-reviewed sources). If sources disagree, say so. Never present one side as settled.

## 2. Sub keyword analysis

For each sub keyword, decide:

- **Same intent** as the main keyword (just another way of saying it) → merge into the main sections, no separate H2.
- **Different intent** (different audience, use case, platform, device, or stage) → give it its own H2.

Write the reason for each decision in one short line.

## 3. Outline rules

- **Only the H2 that answers the main intent gets H3s.** Other H2s stay flat by default, even if they have several sub-points. Split them into H3s only when the content is genuinely long or complex.
- At least one major H2 includes the main keyword, when it reads naturally.
- Always end with:
  - `H2: FAQs` with 3 to 5 questions as H3s (mix openers, not all "Can I...").
- **FAQs must not overlap the body.** Each FAQ question must cover something no H2/H3 in the outline already explains (not even partly, e.g. no "Mac or Windows?" FAQ when the picks or "which fits you" sections already compare them; no specs FAQ when there is a specs H2). After drafting, check every FAQ against every H2/H3 and replace any that overlaps. Good FAQ sources: "People also ask", forum questions, and side concerns found in research (cost, safety, care, legality, lifespan, alternatives).
  - `H2: Conclusion` as the last H2.
- No default "Step" label. Choose by context: "Step 1/2/3" for a fixed sequence, "Tip" for independent advice, plain descriptive H3s otherwise. If unclear, pick the most natural one and mention it.
- Headings are always English. No Vietnamese notes inside headings.
- **Title Case for every heading**: Title, all H2s and all H3s, FAQ questions included ("Why Do I Still Miss Notifications Even With Sound On?"). Capitalize every word except articles (a, an, the), short conjunctions (and, but, or, nor), and prepositions of three letters or fewer (as, at, by, for, in, of, on, to, via), unless it is the first word. Prepositions of four letters or more are capitalized (With, Into, From, Without).

### Vary the structure (do not repeat the same skeleton)

Copy the shape top-ranking pages actually use for this keyword, not one fixed template. Before outlining:

1. Read the outlines in `outlines/` (if the folder exists) and glance at recent `articles/*.md` headings.
2. Make sure the new outline does not reuse the same skeleton as the last few (e.g. "Check the Basics First → How to X for A → How to X for B → FAQs → Conclusion").

Pick the shape that fits the search intent. Examples of different shapes:

| Intent | Possible shape |
|---|---|
| Fix / troubleshoot | Quick checks (H3s) → fixes by scenario → when nothing works |
| How-to (single process) | What you need → the process (Step H3s) → mistakes to avoid |
| List / "best" / "near me" | Picks as H3s under one H2 → how to choose → where/when to find deals |
| Explainer / "what is" | Definition → how it works → pros & cons table → who it suits |
| Comparison / "vs" | Quick verdict → head-to-head by criterion → which to pick |
| Health / safety | What the evidence says → risks / who should avoid → what experts disagree on |

These are starting points, not templates. Mix, reorder, or drop sections based on research.

## 4. Title

- Contains the main keyword **exactly** as given (same word order).
- Not just the bare keyword: add a modifier or hook (year, number, "Easy Fixes", "Complete Guide", "That Actually Work", audience...).
- No parentheses.
- Short enough to rank well (aim for about 50 to 65 characters).
- Title Case.
- Give 2 to 3 options when useful, mark the recommended one, and explain in one line why.

## 5. Output format

Write the explanations in Vietnamese, outside the outline. Use this order:

1. **Research finding** (Vietnamese, short bullets): which pages were read (with URLs), the dominant structure, gaps, and any important warnings / misconceptions / conflicting opinions.
2. **Phân loại sub keyword** (Vietnamese): one line per sub keyword → gộp or tách H2, with the reason.
3. **Title options** (Vietnamese reasoning, English titles).
4. **Outline** in a code block, exactly this format (label every heading with `H2:` / `H3:`, no bullets or `*` before H3s):

```
Title: How to Unsilence Notifications on iPhone
H2: Check the Basics First
H3: Ring/Silent Switch
H3: Volume and Sound Settings
H3: Do Not Disturb or Focus Mode
H2: How to Unsilence Notifications for a Specific Contact
H2: How to Unsilence Notifications for a Specific App
H3: Step 1: Go to Settings and Tap Notifications
H3: Step 2: Select the App
H3: Step 3: Turn On Allow Notifications and Sounds
H2: FAQs
H3: Why Do Notifications From Unknown Senders Stay Silent Even After I Fix Settings?
H3: Does Sleep Focus Silence Notifications Differently Than Do Not Disturb?
H3: Is It Possible to Unsilence Just One Focus Mode Without Turning Off All of Them?
H3: Why Do I Still Miss Notifications Even With Sound On?
H2: Conclusion
```

(This is a format example only. Do not reuse its structure.)

5. Save the final outline (title + outline block + main/sub keywords) to `outlines/<keyword-slug>.md` so later outlines can be checked for variety.
6. End with exactly: **Bạn muốn viết content phần nào trước?**
