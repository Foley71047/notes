# CLAUDE.md —— Foley的笔记

王乐圆（Leyuan Wang，南开大学物理学院，量子信息方向）的个人知识网站。
用 [Zensical](https://zensical.org/docs/) 构建，部署在 <https://notes.leyuanwang.tech/>（子域名根目录）。

| 站点 | 网址 | 仓库 |
|---|---|---|
| 笔记（本仓库） | <https://notes.leyuanwang.tech/> | `foley71047/notes` |
| 个人主页 | <https://leyuanwang.tech/> | `foley71047/foley71047.github.io`（仓库里的 `CNAME` 文件不要删） |

旧地址 `foley71047.github.io/notes/` 已停用。

## 常用命令

```sh
pip install zensical
python scripts/site_data.py          # 检查所有笔记和概念的元数据（类型、标签清单、前置知识链接），有错误时退出码为 1
zensical serve                       # 本地预览（地址见终端输出）
zensical build --clean --strict      # 严格构建：有失效链接或警告即失败（提交前必须通过）
```

- 推送到 `main` 后，`.github/workflows/docs.yml` 先运行 `python scripts/site_data.py` 检查元数据，再构建并部署到 GitHub Pages。
- 站点地址只在 `zensical.toml` 的 `site_url` 里写一次（`https://notes.leyuanwang.tech/`）。
  自定义域名在仓库 Settings → Pages → Custom domain 里设置；用 Actions 部署时 `CNAME` 文件会被忽略，所以本仓库不放 `CNAME`。
- 不要写死 `/notes/` 前缀或站点域名：站内链接一律用相对 `.md` 路径；回个人主页用 `https://leyuanwang.tech`（页脚在 `zensical.toml` 的 `[[project.extra.social]]`）。
- 提交作者用 `Leyuan Wang <3488591540mancity@gmail.com>`（`git config user.name/user.email`）；提交信息和 PR 描述不要添加 Co-Authored-By、Claude-Session 或任何 Claude 署名。

## 网站结构

顶部导航五项：**首页 · 笔记 · 概念 · 标签 · 关于**（`docs/.nav.yml`，awesome-nav 插件）。
`docs/notes/` 和 `docs/concepts/` 里的文件**自动收录**，新增文章不改任何导航或列表。

```
zensical.toml                 # 全部配置：主题、插件、Markdown 扩展、笔记类型、标签清单、旧网址跳转
docs/
  .nav.yml                    # 顶部导航（五项）
  index.md                    # 首页（hero + 三张入口卡片 + 最近更新）
  notes/                      # 笔记：思考 / 论文阅读 / 有的没的，全部平铺在这里
    index.md                  #   入口页：一句话简介 + 自动生成的筛选按钮和笔记列表
    .meta.yml                 #   本目录共用 front matter（隐藏左侧栏）
    <note>.md  <note>.pdf  images/
  concepts/                   # 概念词条：每个文件一个定理 / 不等式 / 结论 / 基本概念
    index.md                  #   入口页：自动生成的速查表（按英文名首字母排序；列：英文名 / 中文名 / 简介）
    .meta.yml
    <concept>.md
  tags.md                     # 标签页（自动生成：全部标签及文章数；点开一个标签列出相关笔记和概念）
  about/
    index.md                  # 关于：简介、主页链接
    writing-template.md       # 写作模板：元数据字段、要点框、概念词条模板、悬停预览、各种写法
  stylesheets/extra.css       # 全部自定义样式（配色变量在文件开头）
  javascripts/mathjax.js      # MathJax 配置（ams 编号、\ket 等宏；悬停预览里的公式排版）
  javascripts/site.js         # 笔记类型筛选、标签页单标签视图
  assets/                     # logo.svg / favicon.svg
overrides/partials/content.html  # 模板覆盖：把生成的信息栏插到标题下、列表插到正文后
scripts/site_data.py          # 构建时生成列表、信息栏、标签页、反向链接；命令行运行时检查元数据
inbox/                        # 待整理的原始文件（不会发布；整理完即删除）
```

- 不要创建空页面或占位页面；规划中的内容不建页面。
- 作者明确不公开的文件不要放进 `docs/`（`docs/` 里的一切都会发布）。

### 自动生成的内容是怎么来的

`zensical.toml` 的 `[project.plugins.macros]` 让 Zensical 在渲染每页前调用 `scripts/site_data.py` 的 `define_env()`。
它扫描 `docs/notes/`、`docs/concepts/` 的 front matter 和 git 日期，把 HTML 写进 `page.meta["fl"]`（`bar` 放在一级标题下，`after` 放在正文后），
由 `overrides/partials/content.html` 插进页面。正文里**不使用宏**（宏语法换成了 `{fl{ }fl}`，LaTeX 里的 `{{ }}` 不受影响）。

- 笔记入口页、概念速查表、标签页、首页"最近更新"、每篇笔记的信息栏（类型、更新日期、前置知识）和底部标签、概念词条的英文名/标签和"引用本概念的笔记"，都由这里生成。**不要手写这些内容。**
- 更新日期 = 该文件最后一次 git 提交的日期（`--follow` 跟踪改名）；有未提交改动时显示今天。CI 需要 `fetch-depth: 0`。
- "引用本概念的笔记"= 正文里有指向该词条 `.md` 的链接的笔记。
- `zensical.toml` 的 `watch` 让笔记或概念改动时整站重新生成；如果本地预览里列表没更新，重启 `zensical serve` 或运行 `zensical build --clean`。
- 获取当前页面依赖 Zensical 内部的 `ContextExtension`（见 `current_page()` 的注释）。升级 Zensical 后若构建报"找不到当前页面"，先看这里。

### 旧网址

改版前的 `research/…`、`tutorials/`、`interests/…` 页面，以及改名前的 `theorems/…`，在 `zensical.toml` 的 `[project.plugins.redirects.redirect_maps]` 里跳转到新地址。
以后移动或改名页面时也在这里加一条，避免失效链接。（PDF 等非页面文件无法跳转。）
**删除或改名页面时要检查这张表**：构建工具不会自动清理跳转，目标文件不存在时严格构建会失败（"Redirect target … does not exist"）。删除页面就删掉以它为目标的行（或改成跳到 `notes/index.md`），改名就改目标并加一条"旧名 → 新名"。

### 改哪一页在哪个文件

| 页面 | 文件 |
|---|---|
| 首页（hero 文字、三张入口卡片） | `docs/index.md`（"最近更新"列表自动生成） |
| 笔记入口页（标题和一句话简介） | `docs/notes/index.md`（列表自动生成） |
| 某篇笔记 | `docs/notes/<文件名>.md`（信息栏来自 front matter） |
| 概念入口页 / 某个概念 | `docs/concepts/index.md` / `docs/concepts/<文件名>.md` |
| 标签页（标题和简介） | `docs/tags.md`；标签清单在 `zensical.toml` 的 `tag_groups` |
| 关于 / 写作模板 | `docs/about/index.md` / `docs/about/writing-template.md` |
| 网站名、页脚、顶部导航 | `zensical.toml`（`site_name`、`copyright`、`extra.social`）、`docs/.nav.yml` |
| 颜色、字体、样式 | `docs/stylesheets/extra.css` |
| logo / 浏览器图标 | `docs/assets/logo.svg` / `docs/assets/favicon.svg` |
| 自动生成的列表、信息栏、标签页的结构和文字 | `scripts/site_data.py` |

## 笔记

### 类型（front matter 的 `type`，必填，只能取这三个值）

| 类型 | 写什么 |
|---|---|
| `思考` | 自己的推导、研究总结和想法 |
| `论文阅读` | 一篇论文的问题、方法、结论与疑问 |
| `有的没的` | 学业以外的内容和零散杂记（比如量化交易） |

类型清单在 `zensical.toml` 的 `[project.extra] note_types`，同时是笔记入口页的筛选按钮（顺序即按钮顺序，数字自动统计）。
加一类：在列表里加一项，笔记里写 `type: 新类型`；改名或删除：同时改掉用到旧名字的笔记，否则检查脚本报错；并同步更新这张表和写作模板。
"全部"两字在 `scripts/site_data.py` 的 `notes_list()`，按钮样式在 `extra.css` 的"类型筛选按钮"一节。拿不准类型或是否该公开时先问作者，不要自行决定。

### 元数据字段

```yaml
---
description: 一句话摘要              # 必填：笔记列表、首页"最近更新"、搜索结果
type: 思考                           # 必填：思考 / 论文阅读 / 有的没的
tags: [器件无关, 纠缠]               # 必填：2–4 个，只能用下面清单里的
prerequisites:                       # 可选：信息栏"前置知识"
  - ../concepts/chsh-inequality.md   #   站内页面写相对 .md 路径，显示为该页标题的链接
  - 线性代数                          #   其他原样显示
---
```

- **全站不使用成熟度、理解度、完成度之类的状态标记**，不要加这类字段、标签或样式。
- 不要手写更新日期或 `revision_date`，它们自动生成。本站不显示阅读时长。

### 新增笔记的步骤

1. 在 `docs/notes/` 下新建文件，文件名用英文或拼音小写加连字符（`self-testing-review.md`），**标题保留中文**，写在第一个 `#` 里；
2. 写 front matter（上面的字段）；长文可在副标题后放 `!!! keypoints "要点"` 提示框；
3. 提到有词条的概念时链接到词条（`[CHSH 不等式](../concepts/chsh-inequality.md)`），会自动得到悬停预览和反向链接；
4. 运行 `python scripts/site_data.py` 和 `zensical build --clean --strict`。

PDF 与介绍页同目录同名（`xxx.md` + `xxx.pdf`），介绍页里写摘要和章节目录（PDF 内容不进搜索），
嵌入代码见 `docs/about/writing-template.md`。按钮和 `<iframe src>` 都直接写文件名，构建时自动换算路径。

## 概念

- 每个词条是一个**定理、不等式、结论**（CHSH 不等式、Tsirelson 界……）或一个**基本概念**（纠缠熵、POVM……）。概念词条可以和同名标签并存：标签用来归类，词条用来解释。
- 不要批量生成词条；只在作者需要时逐个添加。
- 文件名用英文小写加连字符（`tsirelson-bound.md`），标题（中文名）写在第一个 `#` 里。

```yaml
---
en: Tsirelson's bound                                   # 必填：英文名（速查表按它的首字母分组排序）
statement: '量子力学中 CHSH 值满足 $\lvert S\rvert\le 2\sqrt2$'   # 必填：简介（一两句陈述或定义），速查表第三列；可含公式，用单引号
description: 一句话说明（用于搜索和 SEO）
tags: [Bell 非局域性, 半定规划]                          # 1–4 个，只能用清单里的
---
```

正文结构二选一：
- **定理类**：`!!! theorem "陈述"` 框 → `## 直观含义` → `## 成立条件` → `## 证明思路` → `## 何时取等` → `## 相关结果`；
- **概念类**：`!!! definition "定义"` 框 → `## 直观含义` → `## 例子` → `## 相关结果`。

英文名和标签（标题下）、"引用本概念的笔记"（文末）自动生成，不要手写。

**悬停预览**：`zensical.toml` 里的 `zensical.extensions.preview` 让所有指向 `docs/concepts/*.md` 的站内链接带上即时预览，
鼠标悬停时弹出词条开头（一级标题到第一个 `##` 之间：英文名、标签、陈述 / 定义框），`mathjax.js` 负责排版卡片里的公式。
只有写成链接的名字才有预览；没有纯文本自动识别。

## 标签

标签只表示**主题或方法**，不表示类型（用 `type`）或状态。固定清单如下，**新增标签先加进清单**
（`zensical.toml` 的 `[project.extra.tag_groups]` 和这里同时改），`python scripts/site_data.py` 会拒绝清单外的标签。

| 类别 | 标签 |
|---|---|
| 主题 | `纠缠` `Bell 非局域性` `导引` `器件无关` `相干性` `资源理论` `量子测量` `量子态层析` `线性光学` |
| 方法 | `数值优化` `半定规划` |
| 兴趣 | `量化` |

笔记每篇 2–4 个（少于 2 个时检查脚本只警告），概念词条 1–4 个。

## 写作约定

- **公式**：行内 `$...$`，独立 `$$...$$`（单独成段）；编号公式直接写 `\begin{equation}...\end{equation}`
  （外面不套 `$$`），用 `\label{}`/`\eqref{}` 引用。表格里公式中的竖线写 `\vert`，否则会拆开单元格。
  可用宏：`\ket{}`、`\bra{}`、`\braket{}{}`、`\Tr`。
- **提示框**：`!!! 类型 "中文标题"`，`???` 折叠、`???+` 可折叠默认展开。**必须写中文标题**。

  | 类型 | 用途 | 颜色 |
  |---|---|---|
  | `keypoints` | 要点（放在笔记开头，三五条结论） | 墨绿（强调色，底色略深） |
  | `definition` | 定义 | 墨绿 |
  | `theorem` / `lemma` / `corollary` / `proposition` | 定理类（正文斜体） | 深青绿 |
  | `proof` | 证明（结尾自动加 ∎，通常用 `???` 折叠） | 灰 |
  | `example` | 例题 | 蓝灰 |
  | `warning` | 注意 | 砖红 |
  | `summary` | 总结 | 暗金 |
  | `note` / `tip` / `danger` | 备注 / 提示 / 危险 | 灰绿 / 灰绿 / 深砖红 |

- **副标题**：标题下一行写一句话，下一行 `{ .page-lead }`。
- **长文分部分**：`**第一部分** 标题` 下一行 `{ .part-divider }`（不要用多个一级标题）。
- **Obsidian 语法**要转成标准 Markdown：`[[页面]]` → `[页面](page.md)`，`![[图.png]]` → `![](images/图.png)`；
  图片放在文章同目录的 `images/` 下。
- 站内链接写相对 `.md` 路径，构建时会校验。
- 标题旁不显示 ¶（"本节链接"）；`zensical.toml` 里没有开 `toc.permalink`，不要加回来。
- 代码块写语言名（` ```python `），可加 `title="..."`、`linenums="1"`、`hl_lines="2 3"`。

## 配色与字体

配色风格为"书卷墨绿"：纸色背景、墨色正文、墨绿强调。所有颜色都是 `docs/stylesheets/extra.css`
开头的 `--fl-*` 变量（浅色一组、深色一组），其余规则只引用变量，改色只改这里。
正文、次要文字、强调色、提示框标题和代码高亮与背景的对比度都满足 WCAG AA（≥ 4.5:1），改色后要重新核对。

| 用途 | 变量 | 浅色 | 深色（夜读） |
|---|---|---|---|
| 页面背景 | `--fl-bg` | `#F6F3EA` 纸色 | `#161B18` |
| 顶栏、侧栏、卡片、代码块、表头 | `--fl-surface` | `#ECE6D6` | `#1F2622` |
| 正文 | `--fl-text` | `#1E2A23` 墨色 | `#E8E4D8` 米色 |
| 次要文字（日期、简介、说明） | `--fl-text-2` | `#5B6660` | `#A3ABA5` |
| 强调（链接、按钮、当前导航、标签文字） | `--fl-accent` | `#2F6B4F` 墨绿 | `#7DBF9C` 浅墨绿 |
| 链接悬停 | `--fl-accent-hover` | `#23523C` | `#9ED3B6` |
| 强调色底上的文字（选中的筛选按钮等） | `--fl-on-accent` | `#F6F3EA` | `#161B18` |
| 边框、分隔线 | `--fl-border` | `#D9D1BC` | `#2E3832` |

提示框（同一色系、低饱和）：

| 类型 | 变量 | 浅色 | 深色 |
|---|---|---|---|
| 要点 `keypoints` | `--fl-accent` | `#2F6B4F` 墨绿 | `#7DBF9C` |
| 定义 `definition` | `--fl-def` | `#2F6B4F` 墨绿 | `#7DBF9C` |
| 定理类 `theorem` 等 | `--fl-thm` | `#1D6461` 深青绿 | `#6EC2BA` |
| 证明 `proof` | `--fl-proof` | `#5F6763` 灰 | `#A3ABA5` |
| 例题 `example` | `--fl-ex` | `#4F6A84` 蓝灰 | `#9CB4CF` |
| 注意 `warning` | `--fl-warn` | `#9E4636` 砖红 | `#E3907E` |
| 总结 `summary` | `--fl-sum` | `#7A5E24` 暗金 | `#D8BA6C` |
| 备注 `note` / `tip` | `--fl-note` | `#4F6F62` | `#9DBDAF` |
| 危险 `danger` | `--fl-danger` | `#8E3B2F` | `#EA8272` |

代码高亮用 `--fl-code-*` 变量（关键字、字符串、数字、函数、常量、注释），同样两套。数学公式颜色跟随正文。

- 模式切换：顶栏按钮在 **跟随系统 → 浅色 → 深色** 之间循环，默认跟随系统，选择会记住
  （`zensical.toml` 里的三段 `[[project.theme.palette]]`）。
- Logo / favicon（`docs/assets/logo.svg`、`favicon.svg`）是作者设计的墨色钢笔画（打开的笔记本和小猫，横向、透明背景），不要改动文件本身；
  深色模式下由 `extra.css` 用 `filter: invert(…)` 把顶栏 logo 反相成浅色。
- 首页 hero 右侧的 self-testing 公式在 `docs/index.md` 的 `.fl-hero__formula` 里，窄屏时移到介绍下方；
  MathJax 排版完成前公式是收起的（CDN 加载失败时就不显示），避免 LaTeX 源码压住介绍文字。
- 标题：Source Serif 4 + Noto Serif SC（`extra.css` 顶部 `@import`）
- 正文：Noto Sans SC；代码：JetBrains Mono（`zensical.toml` 的 `theme.font`）
- Google Fonts 加载失败时回退到苹方 / 微软雅黑 / 宋体。
- 卡片：圆角 0.8–1rem、1px 细边框、悬停上移 2px 并出现阴影与墨绿边框。

## 已知限制

- 自动生成依赖 Zensical 的 macros 支持和一个内部接口（`ContextExtension`），见上文"自动生成的内容是怎么来的"。
- 标签页的"单个标签"视图是同一页面上的锚点（`tags/#纠缠`）+ JavaScript 过滤；没有 JavaScript 时所有标签一起显示。
- 搜索界面的少量提示文字（如 "Filters"、"results"）目前只有英文，这是 Zensical 新搜索引擎的现状；中文检索本身正常。
- MathJax 与 Mermaid 从 CDN（jsDelivr / unpkg）加载。
