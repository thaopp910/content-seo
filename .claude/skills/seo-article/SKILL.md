---
name: seo-article
description: Write an English SEO blog article from a title + outline (H2/H3) and keyword list, following the team's content rules (word cap, keyword density, question-style H2s, short sentences, no em dash, scannable layout, FAQ limits, one external link), then deliver it as rich text on the clipboard ready to paste into Google Docs. Use when the user pastes an outline/brief and asks to write an SEO article ("viết bài", "viết bài SEO", "write article from outline").
---

# SEO Article Writer

Turn a brief (title, outline, keywords) into a publish-ready English article with real depth, and deliver it as rich text the user pastes into Google Docs.

## 1. Collect inputs

Read these from the user's message. Use the defaults when something is missing; ask only if the title or outline is missing.

| Input | Default |
|---|---|
| Title (H1) | required |
| Outline (H2/H3) | required |
| Main keyword | taken from the title |
| Secondary keywords | none |
| Max words | 1,200 (whole article, headings included). If the brief says 1,000, the user accepts going up to 1,200 when the extra words add depth. |
| Keyword density | 1% for the main keyword |

Notes written inside the outline (often in Vietnamese, e.g. `> H2 viết dạng câu hỏi`) are rules. Apply them, never print them in the article.

## 2. Research before writing

Always research before writing a single line. Never write from memory alone.

1. Use WebSearch and WebFetch on every topic in the outline: how the thing works, current steps and menu paths, limits, prices, versions, and common problems.
2. Prefer official sources (vendor support pages, documentation, standards bodies, Wikipedia). Cross-check any claim that only one source makes.
3. Read what top-ranking pages cover for the main keyword, to find gaps and real user problems. Do not copy them.
4. Keep a short source list in the scratchpad (claim, source URL). Every specific fact in the article (menu path, number, version, price, requirement) must trace back to a source.
5. If research cannot confirm a fact, leave it out or phrase it generally. Do not guess.
6. After drafting, do a fact-check pass: go through every specific claim in the draft and match it to a source in the list. Fix or remove anything that does not match. Accuracy matters more than word count.

## 3. Writing rules

**Headings**
- H2s are active questions ("How Can Users Fix...?"), not statements. Rewrite outline H2s that are not questions.
- Keep H3 method names from the outline unless they break a rule.
- All H1, H2, and H3 headings use Title Case, FAQ questions included ("Does Any Laptop Work as a Monitor?"). Capitalize every word except articles (a, an, the), short conjunctions (and, but, or, nor), and prepositions of three letters or fewer (as, at, by, for, in, of, on, to, via), unless it is the first word. Prepositions of four letters or more are capitalized (With, Into, From, Without).
- FAQ H3s must not all start the same way. Mix openers: "Does...", "Is it possible...", "How does...", "Which...", "What...". Never all "Can I...".

**Depth (the user's top complaint is "nội dung nông")**
- Do not just list facts. For each point, say why it matters, what it is good or bad at, and when to choose it.
- Add concrete detail: exact menu paths, real limits (e.g. "USB 2.0 cards top out at 1080p 30 fps"), costs as ranges, and gotchas (e.g. PS5 HDCP causes a black screen).
- Explain causes, not only fixes ("Lag usually comes from the network, while a black screen points to settings").
- End sections with a short recommendation ("Competitive players should choose X. Casual players can start with Y.").

**Length**
- Respect the max word count. Plan a budget per section before writing.
- Give each H2 as much depth as the budget allows. If the word cap makes ~200 words per H2 impossible (e.g. 7 H2s under 1,000 words), keep the cap and tell the user which sections are short and what cap would fix it.
- Each FAQ answer: max 80 words (aim for 25 to 50).

**Sentences and flow**
- Short sentences. Aim for under 20 words, never over 25.
- No em dash (—) and no en dash (–) anywhere. Use periods, commas, or "while".
- Use connecting words between sentences and paragraphs: However, As a result, Meanwhile, Similarly, In addition, Fortunately, Still, Now, Otherwise.
- Every H2 opens with 1 to 2 lead sentences before its first H3, list, or table. Give context or a real-world angle ("Gamers often want to... when the TV is busy"), not just facts.
- Lead naturally into the next block ("Now, let's look at each method in practice.").

**Scannable layout (avoid walls of text)**
- Paragraphs of 1 to 3 sentences.
- Use numbered steps for procedures, bullets for checklists and mistakes, tables for comparisons and problem/cause/fix.
- Aim for at least 2 tables and several lists per article.
- Bold only labels in bullets and UI paths (e.g. **Settings > System**). Do not bold keywords, except the main keyword in the intro and the conclusion, which must be bold.

**Keywords**
- Main keyword: about 1% density (1,000 words means about 10 uses, variants included). It must appear, in bold, in the intro and the conclusion.
- Secondary keywords: each appears at least once, naturally, in body text. If one already appears in a heading, that counts and you can skip it.
- Never stuff keywords into one paragraph.

**Accuracy and naming**
- Capitalize brands and product names correctly: Samsung, Android, iPhone, iPad, macOS, Windows, AirPlay, Wi-Fi, USB-C, HDMI, PS5, Xbox, Nintendo Switch, YouTube, etc.
- State only facts confirmed in the research step (menu paths, OS versions, prices as ranges). Drop any claim you could not verify.

**External links**
- Add exactly 1 external link to an authoritative source (Wikipedia or an official vendor page). Anchor it on the relevant term. Mention other tools by name without linking.
- Prefer a URL you are certain of (Wikipedia is safest). Do not link to competitors' blogs.

**Structure**
1. Meta description at the very top, before the H1, written as `> Meta description: ...`. Max 160 characters, includes the exact main keyword, and works as a one-line pitch of the article.
2. H1 title
3. Intro (50 to 80 words, includes the main keyword)
4. H2 sections in outline order
5. FAQs (H2) with H3 questions
6. Conclusion (40 to 70 words, includes the main keyword, ends with a clear takeaway)

## 4. Draft and check

1. Write the draft as Markdown in the repo at `articles/<slug>.md`.
2. Run the checker:
   ```bash
   python3 .claude/skills/seo-article/scripts/check_article.py articles/<slug>.md \
     --max-words 1200 --main "laptop as monitor" --main "laptop as a monitor" \
     --secondary "how to use a laptop as a monitor" --secondary "how to use laptop as second monitor"
   ```
   Pass every variant of the main keyword with `--main`.
3. Fix every FAIL (word count, dashes, density, missing intro/conclusion keyword, missing secondary keyword, FAQ over 80 words, long sentences, more than 1 external link). Re-run until it passes.

See `references/example-article.md` for an article that passes all the rules.

## 5. Deliver as rich text

The user pastes the article into Google Docs themselves. Do not use the Google Drive/Docs connectors (they need an OAuth login the user prefers to skip), unless the user asks for it.

```bash
python3 .claude/skills/seo-article/scripts/md_to_clipboard.py articles/<slug>.md
```

This writes `articles/<slug>.html`, copies it to the macOS clipboard as rich text, and opens it in the browser. Tell the user to open a blank Google Doc (`docs.new`) and press **Cmd + V**. Headings, lists, tables, bold, and the link carry over. If the clipboard gets overwritten, they can press Cmd + A, Cmd + C on the opened HTML page.

## 6. Report back

Reply in the user's language (usually Vietnamese) with:
- That the article is on the clipboard, ready to paste into Google Docs, plus the file paths.
- Checker results: total words, main keyword count and density, words per H2.
- Any trade-off made (e.g. H2s under 200 words because of the word cap) and the main sources used. Flag any fact where sources disagreed.
