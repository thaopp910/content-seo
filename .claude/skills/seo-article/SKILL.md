---
name: seo-article
description: Write an English SEO blog article from a title + outline (H2/H3) and keyword list, following the team's content rules (word cap, keyword density, question-style H2s, short sentences, no em dash, scannable layout, FAQ limits, external links), then publish it as a Google Doc in Google Drive. Use when the user pastes an outline/brief and asks to write an SEO article ("viết bài", "viết bài SEO", "write article from outline").
---

# SEO Article Writer

Turn a brief (title, outline, keywords) into a publish-ready English article and deliver it as a Google Doc.

## 1. Collect inputs

Read these from the user's message. Use the defaults when something is missing; ask only if the title or outline is missing.

| Input | Default |
|---|---|
| Title (H1) | required |
| Outline (H2/H3) | required |
| Main keyword | taken from the title |
| Secondary keywords | none |
| Max words | 1,000 (whole article, headings included) |
| Keyword density | 1% for the main keyword |
| Google Drive folder | Drive root |

Notes written inside the outline (often in Vietnamese, e.g. `> H2 viết dạng câu hỏi`) are rules. Apply them, never print them in the article.

## 2. Writing rules

**Headings**
- H2s are active questions ("How Can Users Fix...?"), not statements. Rewrite outline H2s that are not questions.
- Keep H3 method names from the outline unless they break a rule.
- FAQ H3s must not all start the same way. Mix openers: "Does...", "Is it possible...", "How does...", "Which...", "What...". Never all "Can I...".

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
- Bold only labels in bullets and UI paths (e.g. **Settings > System**). Do not bold keywords.

**Keywords**
- Main keyword: about 1% density (1,000 words means about 10 uses, variants included). It must appear in the intro and the conclusion.
- Secondary keywords: each appears at least once, naturally, in body text. If one already appears in a heading, that counts and you can skip it.
- Never stuff keywords into one paragraph.

**Accuracy and naming**
- Capitalize brands and product names correctly: Samsung, Android, iPhone, iPad, macOS, Windows, AirPlay, Wi-Fi, USB-C, HDMI, PS5, Xbox, Nintendo Switch, YouTube, etc.
- State only facts you are confident in (menu paths, OS versions, prices as ranges). Avoid exact claims you cannot verify.

**External links**
- Add 2 to 3 external links to authoritative sources (official vendor support pages, Wikipedia, standards bodies). Anchor them on the relevant term.
- Do not link to competitors' blogs. Flag any URL you are unsure of so the user can check it.

**Structure**
1. H1 title
2. Intro (50 to 80 words, includes the main keyword)
3. H2 sections in outline order
4. FAQs (H2) with H3 questions
5. Conclusion (40 to 70 words, includes the main keyword, ends with a clear takeaway)

## 3. Draft and check

1. Write the draft as Markdown in the scratchpad directory (e.g. `article.md`).
2. Run the checker:
   ```bash
   python3 .claude/skills/seo-article/scripts/check_article.py article.md \
     --max-words 1000 --main "laptop as monitor" --main "laptop as a monitor" \
     --secondary "how to use a laptop as a monitor" --secondary "how to use laptop as second monitor"
   ```
   Pass every variant of the main keyword with `--main`.
3. Fix every FAIL (word count, dashes, density, missing intro/conclusion keyword, missing secondary keyword, FAQ over 80 words, long sentences). Re-run until it passes.

See `references/example-article.md` for an article that passes all the rules.

## 4. Publish to Google Docs

1. Load the `anthropic-skills:google-workspace` skill before any Google Drive or Docs call.
2. Create a new Google Doc named after the H1 title (in the requested folder, else Drive root).
3. Insert the article with real formatting: H1 as Title/Heading 1, H2 as Heading 2, H3 as Heading 3, real bulleted and numbered lists, real tables, and hyperlinks on the external link anchors. Do not paste raw Markdown symbols (`#`, `**`, `|`).
4. Read the doc back once to confirm headings, tables, and links rendered.
5. If no Google Drive/Docs connector is available, tell the user to connect Google Drive in their Claude settings. Meanwhile, save the Markdown file in the repo under `articles/<slug>.md` and give them the path.

## 5. Report back

Reply in the user's language (usually Vietnamese) with:
- The Google Doc link.
- Checker results: total words, main keyword count and density, words per H2.
- Any trade-off made (e.g. H2s under 200 words because of the word cap) and URLs the user should verify.
