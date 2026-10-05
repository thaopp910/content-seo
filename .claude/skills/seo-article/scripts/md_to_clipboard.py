#!/usr/bin/env python3
"""Convert an article Markdown file to HTML and copy it to the macOS clipboard as rich text.

Usage: md_to_clipboard.py articles/<slug>.md
Writes articles/<slug>.html next to the input, copies it as HTML, and opens it in the browser.
Pasting into a blank Google Doc keeps headings, lists, tables, bold, and links.
"""
import html
import re
import subprocess
import sys


def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def convert(lines):
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"(#{1,3}) (.*)", l)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inl(m.group(2))}</h{n}>")
            i += 1
            continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"\|[-| ]+\|$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            t = '<table border="1" style="border-collapse:collapse">'
            for k, r in enumerate(rows):
                tag = "th" if k == 0 else "td"
                cell = (lambda c: f"<b>{inl(c)}</b>") if k == 0 else inl
                t += "<tr>" + "".join(f"<{tag}>{cell(c)}</{tag}>" for c in r) + "</tr>"
            out.append(t + "</table>")
            continue
        if l.startswith("- ") or re.match(r"\d+\. ", l):
            ol = not l.startswith("- ")
            items = []
            while i < len(lines) and (re.match(r"\d+\. ", lines[i]) if ol else lines[i].startswith("- ")):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                i += 1
            tg = "ol" if ol else "ul"
            out.append(f"<{tg}>" + "".join(f"<li>{inl(x)}</li>" for x in items) + f"</{tg}>")
            continue
        if l.strip():
            out.append(f"<p>{inl(l)}</p>")
        i += 1
    return '<html><head><meta charset="utf-8"></head><body>' + "\n".join(out) + "</body></html>"


def main():
    src = sys.argv[1]
    dst = re.sub(r"\.md$", "", src) + ".html"
    page = convert(open(src, encoding="utf-8").read().splitlines())
    open(dst, "w", encoding="utf-8").write(page)
    hexdata = page.encode("utf-8").hex()
    subprocess.run(["osascript", "-e", f"set the clipboard to «data HTML{hexdata}»"], check=True)
    subprocess.run(["open", dst])
    print(f"Wrote {dst} and copied it to the clipboard as rich text")


if __name__ == "__main__":
    main()
