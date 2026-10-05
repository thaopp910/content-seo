#!/usr/bin/env python3
"""Check a Markdown SEO article against the team's writing rules."""
import argparse
import re
import sys


def words(text):
    text = re.sub(r"\]\([^)]*\)", "]", text)  # drop link URLs
    text = re.sub(r"[#*|>\[\]`]+|-{2,}|^\s*-\s", " ", text, flags=re.M)
    return text.split()


def count(text, phrases):
    low = text.lower()
    return sum(len(re.findall(r"\b" + re.escape(p.lower()) + r"\b", low)) for p in phrases)


def sections(lines, level):
    """Yield (heading, body_lines) for headings of the given level."""
    prefix = "#" * level + " "
    head, body = None, []
    for line in lines:
        if line.startswith(prefix):
            if head:
                yield head, body
            head, body = line[len(prefix):].strip(), []
        elif re.match(r"#{1,%d} " % (level - 1), line):
            if head:
                yield head, body
            head, body = None, []
        elif head:
            body.append(line)
    if head:
        yield head, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--max-words", type=int, default=1200)
    ap.add_argument("--main", action="append", default=[], help="main keyword (repeat for variants)")
    ap.add_argument("--secondary", action="append", default=[])
    ap.add_argument("--density", type=float, default=1.0, help="target main keyword density in percent")
    ap.add_argument("--max-sentence", type=int, default=25)
    ap.add_argument("--max-links", type=int, default=1, help="max external links")
    args = ap.parse_args()

    text = open(args.file, encoding="utf-8").read()
    lines = text.splitlines()
    fails = []

    total = len(words(text))
    print(f"Total words: {total} (max {args.max_words})")
    if total > args.max_words:
        fails.append(f"Over word limit by {total - args.max_words}")

    links = re.findall(r"\]\((https?://[^)]+)\)", text)
    print(f"External links: {len(links)} (max {args.max_links})")
    if len(links) > args.max_links:
        fails.append(f"Too many external links ({len(links)})")

    if "—" in text or "–" in text:
        fails.append("Contains em dash or en dash")

    if args.main:
        hits = count(text, args.main)
        density = hits / total * 100 if total else 0
        print(f"Main keyword: {hits} uses, {density:.2f}% density (target {args.density}%)")
        if density < args.density * 0.7 or density > args.density * 2:
            fails.append(f"Main keyword density {density:.2f}% is far from {args.density}%")

        paras = [l for l in lines if l.strip() and not l.startswith(("#", "|", "-", ">"))]
        if paras and not count(paras[0], args.main):
            fails.append("Main keyword missing from intro")
        concl = next((b for h, b in sections(lines, 2) if h.lower().startswith("conclusion")), None)
        if concl is None:
            fails.append("No Conclusion H2")
        elif not count("\n".join(concl), args.main):
            fails.append("Main keyword missing from conclusion")

    for kw in args.secondary:
        n = count(text, [kw])
        print(f"Secondary '{kw}': {n}")
        if not n:
            fails.append(f"Secondary keyword missing: {kw}")

    print("\nWords per H2:")
    for head, body in sections(lines, 2):
        print(f"  {len(words(chr(10).join(body))):4d}  {head}")
        if head.lower() not in ("faqs", "faq", "conclusion") and not head.endswith("?"):
            fails.append(f"H2 is not a question: {head}")

    small = {"a", "an", "the", "and", "but", "or", "nor", "as", "at", "by", "for", "in", "of", "on", "to", "via", "vs"}
    for line in lines:
        m = re.match(r"#{1,3} (.*)", line)
        if not m:
            continue
        for k, w in enumerate(re.findall(r"[A-Za-z][\w'-]*", m.group(1))):
            if w[0].islower() and (k == 0 or w.lower() not in small):
                fails.append(f"Heading not in Title Case ('{w}'): {m.group(1)}")
                break

    faq = next((b for h, b in sections(lines, 2) if h.lower().startswith("faq")), None)
    if faq:
        openers = []
        for q, ans in sections(faq, 3):
            n = len(words("\n".join(ans)))
            openers.append(q.split()[0].lower() + " " + (q.split()[1].lower() if len(q.split()) > 1 else ""))
            if n > 80:
                fails.append(f"FAQ answer over 80 words ({n}): {q}")
        if len(openers) > 1 and len(set(openers)) == 1:
            fails.append(f"All FAQ questions start with '{openers[0]}'")

    for line in lines:
        if line.startswith(("#", "|")):
            continue
        for s in re.split(r"(?<=[.!?:])\s+", line):
            n = len(words(s))
            if n > args.max_sentence:
                fails.append(f"Long sentence ({n} words): {s[:80]}...")

    print()
    if fails:
        for f in fails:
            print("FAIL:", f)
        sys.exit(1)
    print("PASS: all checks")


if __name__ == "__main__":
    main()
