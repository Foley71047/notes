"""生成站点元数据：首页"最近更新"列表，以及每页的"最后更新"时间。

用法：
    python scripts/site_meta.py           # 只刷新 docs/index.md 里的"最近更新"
    python scripts/site_meta.py --stamp   # 另外把 git 最后提交日期写进每页 front matter
                                          # 的 revision_date（仅在 CI 构建前使用，不要提交）

日期取自 git 最后一次提交；未提交的新文件用今天的日期。
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
HOME = DOCS / "index.md"
RECENT_COUNT = 6

SECTIONS = {"research": "科研", "tutorials": "教程", "interests": "兴趣", "about": "关于"}
# 不进入"最近更新"的页面：首页、标签页、各级 index、关于板块
EXCLUDE_DIRS = {"about"}
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def git_date(path: Path) -> str:
    """文件最后一次提交的日期（YYYY-MM-DD）；有未提交改动或尚未提交时返回今天。"""
    rel = str(path.relative_to(ROOT))
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", rel],
        cwd=ROOT, capture_output=True, text=True, check=False,
    ).stdout.strip()
    if dirty:
        return dt.date.today().isoformat()
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", rel],
        cwd=ROOT, capture_output=True, text=True, check=False,
    ).stdout.strip()
    return out or dt.date.today().isoformat()


def split_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def page_title(meta: dict, body: str, path: Path) -> str:
    if meta.get("title"):
        return str(meta["title"])
    match = re.search(r"^# (.+)$", body, re.M)
    return match.group(1).strip() if match else path.stem


def page_url(path: Path) -> str:
    rel = path.relative_to(DOCS).with_suffix("")
    if rel.name == "index":
        rel = rel.parent
    return f"{rel.as_posix()}/" if str(rel) != "." else "./"


def stamp(path: Path, date: str) -> None:
    """把 revision_date 写入 front matter（主题原生显示为"最后更新"）。"""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    line = f'revision_date: "{date}"'
    if match:
        inner = re.sub(r"^revision_date:.*\n?", "", match.group(1), flags=re.M).rstrip("\n")
        text = f"---\n{inner}\n{line}\n---\n" + text[match.end():]
    else:
        text = f"---\n{line}\n---\n\n" + text
    path.write_text(text, encoding="utf-8")


def recent_block(pages: list[dict]) -> str:
    items = []
    for page in pages[:RECENT_COUNT]:
        desc = (
            f'<span class="fl-recent__desc">{html.escape(page["description"])}</span>'
            if page["description"] else ""
        )
        items.append(
            f'<li><a href="{page["url"]}">'
            f'<span class="fl-recent__date">{page["date"]}</span>'
            f'<span class="fl-recent__title">{html.escape(page["title"])}{desc}</span>'
            f'<span class="fl-recent__section">{page["section"]}</span>'
            f"</a></li>"
        )
    return '<ul class="fl-recent">\n' + "\n".join(items) + "\n</ul>"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stamp", action="store_true", help="写入每页的 revision_date")
    args = parser.parse_args()

    articles = []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        date = git_date(path)
        if args.stamp and path != HOME:
            stamp(path, date)
        if len(rel.parts) < 2 or rel.name == "index.md" or rel.parts[0] in EXCLUDE_DIRS:
            continue
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        articles.append({
            "date": date,
            "title": page_title(meta, body, path),
            "description": str(meta.get("description", "")),
            "section": SECTIONS.get(rel.parts[0], rel.parts[0]),
            "url": page_url(path),
        })

    articles.sort(key=lambda p: (p["date"], p["title"]), reverse=True)
    home = HOME.read_text(encoding="utf-8")
    home = re.sub(
        r"(<!-- recent:start -->\n).*?(<!-- recent:end -->)",
        lambda m: m.group(1) + recent_block(articles) + "\n" + m.group(2),
        home, flags=re.S,
    )
    HOME.write_text(home, encoding="utf-8")
    print(f"最近更新：{len(articles[:RECENT_COUNT])} 篇" + ("；已写入 revision_date" if args.stamp else ""))


if __name__ == "__main__":
    main()
