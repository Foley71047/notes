"""站点数据：扫描 docs/notes/ 与 docs/theorems/，生成列表、信息栏和反向链接。

作者只需要填 front matter，其余内容都在构建时由这里生成：

- 笔记入口页（notes/index.md）：类型筛选按钮 + 按更新时间倒序的笔记列表；
- 每篇笔记：标题下的信息栏（类型、更新日期、阅读时长、前置知识）与文末标签；
- 定理入口页（theorems/index.md）：按拼音排序的速查表；
- 每个定理词条：标题下的英文名与标签，文末"引用本定理的笔记"；
- 标签页（tags.md）：全部标签及文章数，每个标签下的笔记与定理；
- 首页（index.md）："最近更新"。

两种用法：

1. 构建时：zensical.toml 的 [project.plugins.macros] 让 Zensical 在渲染每个页面前
   调用 define_env()。这里把生成的 HTML 写进 page.meta["fl"]（bar 放在标题下，
   after 放在正文后），由 overrides/partials/content.html 插进页面。
2. 命令行：python scripts/site_data.py 检查所有笔记和定理的元数据
   （类型、标签是否在清单里、前置知识链接是否存在……），有错误时退出码为 1。

允许的类型和标签清单在 zensical.toml 的 [project.extra.note_types] 和
[project.extra.tag_groups] 里。
"""

import datetime as dt
import html
import posixpath
import re
import subprocess
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "zensical.toml"
SECTIONS = ("notes", "theorems")
RECENT_COUNT = 6
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_TARGET = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^)]*)?\)|^\s*\[[^\]]+\]:\s*<?(\S+?)>?\s*$", re.M)


# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------


@dataclass
class Entry:
    """一篇笔记或一个定理词条。"""

    kind: str          # "note" 或 "theorem"
    path: str          # 相对 docs/ 的源文件路径，如 notes/di-primer.md
    url: str           # 相对站点根目录的网址，如 notes/di-primer/
    title: str
    meta: dict
    body: str
    date: str = ""
    minutes: int = 1
    links: set[str] = field(default_factory=set)  # 正文里链接到的站内 .md 文件

    @property
    def tags(self) -> list[str]:
        tags = self.meta.get("tags") or []
        return [str(t) for t in tags] if isinstance(tags, list) else [str(tags)]


@dataclass
class Site:
    notes: list[Entry]
    theorems: list[Entry]
    note_types: list[str]
    tag_groups: dict[str, list[str]]
    errors: list[str]
    warnings: list[str]

    def entry(self, path: str) -> Entry | None:
        for e in self.notes + self.theorems:
            if e.path == path:
                return e
        return None

    def cited_by(self, theorem: Entry) -> list[Entry]:
        return [n for n in self.notes if theorem.path in n.links]

    def tagged(self, tag: str) -> tuple[list[Entry], list[Entry]]:
        return (
            [n for n in self.notes if tag in n.tags],
            [t for t in self.theorems if tag in t.tags],
        )


def split_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    return (meta if isinstance(meta, dict) else {}), text[match.end():]


def page_url(path: str) -> str:
    rel = posixpath.splitext(path)[0]
    if posixpath.basename(rel) == "index":
        rel = posixpath.dirname(rel)
    return f"{rel}/" if rel else ""


def page_title(meta: dict, body: str, path: str) -> str:
    if meta.get("title"):
        return str(meta["title"])
    match = re.search(r"^# (.+?)\s*$", body, re.M)
    return match.group(1).strip() if match else posixpath.basename(path)


def git_dates(paths: list[str]) -> dict[str, str]:
    """每个文件最后一次提交的日期（YYYY-MM-DD）。有未提交改动或尚未提交时用今天。"""
    today = dt.date.today().isoformat()
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all", "--", "docs"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {p: today for p in paths}
    dirty, fields = set(), status.split("\0")
    i = 0
    while i < len(fields):
        item = fields[i]
        if len(item) > 3:
            dirty.add(item[3:])
            if item[0] in "RC":  # 重命名 / 复制：下一项是原路径
                i += 1
        i += 1
    dates = {}
    for path in paths:
        rel = f"docs/{path}"
        if rel in dirty:
            dates[path] = today
            continue
        out = subprocess.run(
            ["git", "log", "-1", "--follow", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip()
        dates[path] = out or today
    return dates


def reading_minutes(body: str) -> int:
    """估算阅读时长：中文每分钟 400 字，英文每分钟 200 词，
    独立公式每个 15 秒、行内公式每个 3 秒，代码块不计。"""
    text = re.sub(r"^(```|~~~).*?^\1", " ", body, flags=re.S | re.M)
    display = r"\$\$.*?\$\$|\\begin\{([a-z]+\*?)\}.*?\\end\{\1\}"
    n_display = len(re.findall(display, text, re.S))
    text = re.sub(display, " ", text, flags=re.S)
    n_inline = len(re.findall(r"\$[^$\n]+\$", text))
    text = re.sub(r"\$[^$\n]+\$", " ", text)
    text = re.sub(r"<[^>]+>|\]\([^)]*\)", " ", text)
    cjk = len(re.findall(r"[㐀-鿿]", text))
    words = len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", text))
    minutes = cjk / 400 + words / 200 + n_display * 0.25 + n_inline * 0.05
    return max(1, round(minutes))


def resolve_link(source: str, target: str) -> str | None:
    """把正文里的相对链接解析成相对 docs/ 的 .md 路径；站外链接返回 None。"""
    target = target.split("#", 1)[0]
    if not target.endswith(".md") or re.match(r"^[a-z]+:|^/", target):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), target))


def pinyin_key(text: str) -> str:
    try:
        from pypinyin import lazy_pinyin
    except ImportError:
        return text.lower()
    return " ".join(lazy_pinyin(text)).lower()


def read_config() -> tuple[list[str], dict[str, list[str]]]:
    extra = tomllib.loads(CONFIG.read_text(encoding="utf-8"))["project"].get("extra", {})
    return list(extra.get("note_types", [])), dict(extra.get("tag_groups", {}))


def collect() -> Site:
    note_types, tag_groups = read_config()
    allowed_tags = {t for tags in tag_groups.values() for t in tags}
    site = Site([], [], note_types, tag_groups, [], [])

    for section in SECTIONS:
        for file in sorted((DOCS / section).rglob("*.md")):
            if file.name == "index.md":
                continue
            path = file.relative_to(DOCS).as_posix()
            try:
                meta, body = split_front_matter(file.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                site.errors.append(f"{path}: front matter 不是合法的 YAML（{exc}）")
                meta, body = {}, file.read_text(encoding="utf-8")
            kind = "note" if section == "notes" else "theorem"
            entry = Entry(kind, path, page_url(path), page_title(meta, body, path), meta, body)
            for match in LINK_TARGET.finditer(body):
                if (target := resolve_link(path, match.group(1) or match.group(2))):
                    entry.links.add(target)
            override = meta.get("reading_time")
            entry.minutes = int(override) if isinstance(override, int) else reading_minutes(body)
            (site.notes if kind == "note" else site.theorems).append(entry)

    dates = git_dates([e.path for e in site.notes + site.theorems])
    for entry in site.notes + site.theorems:
        entry.date = dates[entry.path]
        check(site, entry, allowed_tags)

    site.notes.sort(key=lambda e: (e.date, e.title), reverse=True)
    site.theorems.sort(key=lambda e: pinyin_key(e.title))
    return site


def check(site: Site, entry: Entry, allowed_tags: set[str]) -> None:
    """检查元数据。错误会让 CI 失败；警告只提示。"""
    p, meta = entry.path, entry.meta
    if not re.search(r"^# .+", entry.body, re.M) and not meta.get("title"):
        site.warnings.append(f"{p}: 没有一级标题（# 标题）")
    for tag in entry.tags:
        if tag not in allowed_tags:
            site.errors.append(f"{p}: 标签「{tag}」不在清单里（zensical.toml 的 tag_groups）")
    if entry.kind == "note":
        if meta.get("type") not in site.note_types:
            site.errors.append(
                f"{p}: type 必须是 {' / '.join(site.note_types)} 之一，现在是 {meta.get('type')!r}"
            )
        if not meta.get("description"):
            site.warnings.append(f"{p}: 缺少 description（一句话摘要）")
        if not 2 <= len(entry.tags) <= 4:
            site.warnings.append(f"{p}: 建议 2–4 个标签，现在有 {len(entry.tags)} 个")
        for item in as_list(meta.get("prerequisites")):
            target = resolve_link(p, str(item))
            if target and not (DOCS / target).is_file():
                site.errors.append(f"{p}: 前置知识链接的页面不存在：{item}")
    else:
        for key in ("en", "statement"):
            if not meta.get(key):
                site.errors.append(f"{p}: 定理词条缺少 {key}")
        if not 1 <= len(entry.tags) <= 4:
            site.warnings.append(f"{p}: 建议 1–4 个标签，现在有 {len(entry.tags)} 个")


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


# ---------------------------------------------------------------------------
# HTML 片段
# ---------------------------------------------------------------------------

esc = html.escape


def href(base: str, target: str) -> str:
    """从 base 页面（网址目录，如 notes/a/）指向 target 的相对链接。"""
    target, _, fragment = target.partition("#")
    rel = posixpath.relpath("/" + target, "/" + base) if target != base else "."
    rel = "./" if rel == "." else rel + ("/" if target.endswith("/") or not target else "")
    return rel + (f"#{fragment}" if fragment else "")


def tag_slug(tag: str) -> str:
    return re.sub(r"\s+", "-", tag.strip())


def inline_md(text: str) -> str:
    """把一行 Markdown（可含 $公式$）渲染成行内 HTML。"""
    import markdown

    out = markdown.markdown(
        str(text),
        extensions=["pymdownx.arithmatex", "pymdownx.betterem"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
    )
    return re.sub(r"^<p>(.*)</p>$", r"\1", out.strip(), flags=re.S)


def type_badge(entry: Entry) -> str:
    label = entry.meta.get("type", "定理") if entry.kind == "note" else "定理"
    return f'<span class="fl-type">{esc(str(label))}</span>'


def tag_links(base: str, tags: list[str], cls: str = "md-tag") -> str:
    return "".join(
        f'<a class="{cls}" href="{href(base, "tags/#" + tag_slug(t))}">{esc(t)}</a>' for t in tags
    )


def entry_link(base: str, entry: Entry) -> str:
    preview = " data-preview" if entry.kind == "theorem" else ""
    return f'<a href="{href(base, entry.url)}"{preview}>{esc(entry.title)}</a>'


def note_bar(site: Site, note: Entry, base: str) -> str:
    items = [
        type_badge(note),
        f'<span>更新于 <time datetime="{note.date}">{note.date}</time></span>',
        f"<span>阅读约 {note.minutes} 分钟</span>",
    ]
    prereqs = []
    for item in as_list(note.meta.get("prerequisites")):
        target = resolve_link(note.path, str(item))
        linked = site.entry(target) if target else None
        if linked:
            prereqs.append(entry_link(base, linked))
        elif target and (DOCS / target).is_file():
            prereqs.append(f'<a href="{href(base, page_url(target))}">{esc(str(item))}</a>')
        else:
            prereqs.append(esc(str(item)))
    if prereqs:
        items.append(f'<span>前置知识：{"、".join(prereqs)}</span>')
    return f'<p class="fl-meta">{"".join(items)}</p>'


def theorem_bar(theorem: Entry, base: str) -> str:
    items = [f'<span class="fl-meta__en" lang="en">{esc(str(theorem.meta.get("en", "")))}</span>']
    if theorem.tags:
        items.append(f'<span class="fl-meta__tags">{tag_links(base, theorem.tags, "fl-tag")}</span>')
    return f'<p class="fl-meta fl-meta--theorem">{"".join(items)}</p>'


def page_tags(base: str, entry: Entry) -> str:
    if not entry.tags:
        return ""
    return f'<nav class="md-tags" aria-label="标签">{tag_links(base, entry.tags)}</nav>'


def cited_by(site: Site, theorem: Entry, base: str) -> str:
    notes = site.cited_by(theorem)
    out = ['<h2 id="cited-by">引用本定理的笔记</h2>']
    if notes:
        out.append('<ul class="fl-backlinks">')
        out += [
            f"<li>{entry_link(base, n)}{type_badge(n)}"
            f'<time datetime="{n.date}">{n.date}</time></li>'
            for n in notes
        ]
        out.append("</ul>")
    else:
        out.append('<p class="fl-muted">还没有笔记引用本定理。在笔记里链接到本页，这里会自动出现。</p>')
    return "\n".join(out)


def notes_list(site: Site, base: str) -> str:
    counts = {t: sum(n.meta.get("type") == t for n in site.notes) for t in site.note_types}
    buttons = [
        f'<button type="button" class="fl-filter__btn" data-type="" aria-pressed="true">'
        f'全部<span class="fl-filter__count">{len(site.notes)}</span></button>'
    ] + [
        f'<button type="button" class="fl-filter__btn" data-type="{esc(t)}" aria-pressed="false">'
        f'{esc(t)}<span class="fl-filter__count">{counts[t]}</span></button>'
        for t in site.note_types
    ]
    items = []
    for n in site.notes:
        desc = n.meta.get("description")
        items.append(
            f'<li class="fl-note" data-type="{esc(str(n.meta.get("type", "")))}">'
            f'<a class="fl-note__title" href="{href(base, n.url)}">{esc(n.title)}</a>'
            + (f'<p class="fl-note__desc">{esc(str(desc))}</p>' if desc else "")
            + f'<p class="fl-note__meta">{type_badge(n)}'
            f'<time datetime="{n.date}">{n.date}</time>'
            f"<span>{n.minutes} 分钟</span>"
            f'<span class="fl-note__tags">{tag_links(base, n.tags, "fl-tag")}</span></p></li>'
        )
    return (
        '<div class="fl-notes" data-fl-notes>'
        f'<div class="fl-filter" role="group" aria-label="按类型筛选">{"".join(buttons)}</div>'
        f'<ul class="fl-note-list">{"".join(items)}</ul>'
        '<p class="fl-muted fl-notes__empty" hidden>这一类还没有笔记。</p></div>'
    )


def theorem_table(site: Site, base: str) -> str:
    rows, letter = [], None
    for t in site.theorems:
        initial = (pinyin_key(t.title)[:1] or "#").upper()
        if initial != letter:
            letter = initial
            rows.append(f'<tr class="fl-thm-letter"><th colspan="3">{esc(letter)}</th></tr>')
        rows.append(
            f'<tr><td class="fl-thm-name"><a href="{href(base, t.url)}">{esc(t.title)}</a></td>'
            f'<td class="fl-thm-en" lang="en">{esc(str(t.meta.get("en", "")))}</td>'
            f'<td class="fl-thm-statement">{inline_md(t.meta.get("statement", ""))}</td></tr>'
        )
    if not rows:
        return '<p class="fl-muted">还没有定理词条。</p>'
    return (
        '<div class="fl-thm-index"><table><thead><tr><th>定理</th><th>English</th>'
        f'<th>核心陈述</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def tags_page(site: Site, base: str) -> str:
    used = {t for e in site.notes + site.theorems for t in e.tags}
    groups = {g: [t for t in tags if t in used] for g, tags in site.tag_groups.items()}
    listed = {t for tags in groups.values() for t in tags}
    if others := sorted(used - listed):
        groups["其他"] = others
    index, sections = [], []
    for group, tags in groups.items():
        if not tags:
            continue
        chips = []
        for tag in tags:
            notes, theorems = site.tagged(tag)
            chips.append(
                f'<a class="fl-tag-chip" href="#{esc(tag_slug(tag))}">{esc(tag)}'
                f'<span class="fl-tag-chip__count">{len(notes) + len(theorems)}</span></a>'
            )
            parts = [
                f'<section class="fl-tag-section" id="{esc(tag_slug(tag))}">',
                f'<h2>{esc(tag)}<small>{len(notes)} 篇笔记 · {len(theorems)} 条定理</small></h2>',
            ]
            if notes:
                parts.append("<h3>笔记</h3><ul class=\"fl-backlinks\">")
                parts += [
                    f"<li>{entry_link(base, n)}{type_badge(n)}"
                    f'<time datetime="{n.date}">{n.date}</time></li>'
                    for n in notes
                ]
                parts.append("</ul>")
            if theorems:
                parts.append("<h3>定理</h3><ul class=\"fl-backlinks\">")
                parts += [
                    f'<li>{entry_link(base, t)}<span class="fl-meta__en" lang="en">'
                    f'{esc(str(t.meta.get("en", "")))}</span></li>'
                    for t in theorems
                ]
                parts.append("</ul>")
            parts.append('<p class="fl-tag-back"><a href="./">← 全部标签</a></p></section>')
            sections.append("".join(parts))
        index.append(
            f'<div class="fl-tag-group"><h2>{esc(group)}</h2>'
            f'<p class="fl-tag-cloud">{"".join(chips)}</p></div>'
        )
    return (
        f'<div class="fl-tags" data-fl-tags><div class="fl-tags__index">{"".join(index)}</div>'
        f'{"".join(sections)}</div>'
    )


def recent_list(site: Site, base: str) -> str:
    entries = sorted(site.notes + site.theorems, key=lambda e: (e.date, e.title), reverse=True)
    items = []
    for e in entries[:RECENT_COUNT]:
        desc = e.meta.get("description") if e.kind == "note" else e.meta.get("en")
        items.append(
            f'<li><a href="{href(base, e.url)}">'
            f'<span class="fl-recent__date">{e.date}</span>'
            f'<span class="fl-recent__title">{esc(e.title)}'
            + (f'<span class="fl-recent__desc">{esc(str(desc))}</span>' if desc else "")
            + f'</span><span class="fl-recent__section">{esc(str(e.meta.get("type", "定理")) if e.kind == "note" else "定理")}</span>'
            "</a></li>"
        )
    return f'<ul class="fl-recent">{"".join(items)}</ul>'


def page_parts(site: Site, path: str) -> dict[str, str]:
    """某个页面要插入的 HTML：bar 放在一级标题下，after 放在正文后。"""
    base = page_url(path)
    if path == "index.md":
        return {"after": recent_list(site, base)}
    if path == "tags.md":
        return {"after": tags_page(site, base)}
    if path == "notes/index.md":
        return {"after": notes_list(site, base)}
    if path == "theorems/index.md":
        return {"after": theorem_table(site, base)}
    entry = site.entry(path)
    if entry is None:
        return {}
    if entry.kind == "note":
        return {"bar": note_bar(site, entry, base), "after": page_tags(base, entry)}
    return {"bar": theorem_bar(entry, base), "after": cited_by(site, entry, base)}


# ---------------------------------------------------------------------------
# 构建时入口（Zensical macros）
# ---------------------------------------------------------------------------

# Zensical 每渲染一个页面都会重新执行本文件，所以缓存挂在 sys.modules 上，
# 只有笔记、定理或配置改动后才重新扫描。
_cache = sys.modules.setdefault("_fl_site_data_cache", types.ModuleType("_fl_site_data_cache"))


def signature() -> tuple:
    files = [f for s in SECTIONS for f in (DOCS / s).rglob("*.md")]
    files += [CONFIG, ROOT / ".git" / "index", ROOT / ".git" / "HEAD"]
    return tuple(sorted((str(f), f.stat().st_mtime_ns) for f in files if f.exists()))


def cached_site() -> Site:
    sig = signature()
    if getattr(_cache, "signature", None) != sig:
        site = collect()
        for message in site.errors + site.warnings:
            print(f"[site_data] {message}", file=sys.stderr)
        _cache.signature, _cache.site = sig, site
    return _cache.site


def current_page(env):
    """取当前正在渲染的页面。

    macros 的 define_env() 拿不到页面对象，但 Zensical 在渲染每页前会把页面放进
    ContextExtension（见 zensical/markdown/render.py），这里从配置里把它找出来。
    这依赖 Zensical 的内部实现；将来失效时会直接报错，而不是悄悄生成空页面。
    """
    from zensical.extensions.context import ContextExtension

    for ext in env.conf.get("markdown_extensions", []):
        if isinstance(ext, ContextExtension) and ext._kwargs.get("page") is not None:
            return ext._kwargs["page"]
    raise RuntimeError("scripts/site_data.py：找不到当前页面，Zensical 的内部接口可能变了")


def define_env(env) -> None:
    page = current_page(env)
    path = page.path.replace("\\", "/")
    if path not in ("index.md", "tags.md") and not path.startswith(tuple(f"{s}/" for s in SECTIONS)):
        return
    parts = page_parts(cached_site(), path)
    if parts:
        page.meta["fl"] = parts


# ---------------------------------------------------------------------------
# 命令行：检查元数据
# ---------------------------------------------------------------------------


def main() -> int:
    site = collect()
    for message in site.warnings:
        print(f"警告  {message}")
    for message in site.errors:
        print(f"错误  {message}")
    print(
        f"{len(site.notes)} 篇笔记，{len(site.theorems)} 个定理词条；"
        f"{len(site.errors)} 个错误，{len(site.warnings)} 个警告"
    )
    return 1 if site.errors else 0


if __name__ == "__main__":
    sys.exit(main())
