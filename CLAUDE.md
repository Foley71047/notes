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
python scripts/site_meta.py          # 刷新首页"最近更新"（新增/改名文章后运行并提交）
zensical serve                       # 本地预览（地址见终端输出）
zensical build --clean --strict      # 严格构建：有失效链接或警告即失败（提交前必须通过）
```

- 推送到 `main` 后，`.github/workflows/docs.yml` 自动构建并部署到 GitHub Pages。
- 站点地址只在 `zensical.toml` 的 `site_url` 里写一次（`https://notes.leyuanwang.tech/`）。
  自定义域名在仓库 Settings → Pages → Custom domain 里设置；用 Actions 部署时 `CNAME` 文件会被忽略，所以本仓库不放 `CNAME`。
- 不要写死 `/notes/` 前缀或站点域名：站内链接一律用相对 `.md` 路径；回个人主页用 `https://leyuanwang.tech`（页脚在 `zensical.toml` 的 `[[project.extra.social]]`）。
- CI 会运行 `python scripts/site_meta.py --stamp`，把每页 git 最后提交日期写进
  front matter 的 `revision_date`（主题原生显示为"最后更新"）。**本地不要运行 `--stamp`，
  也不要手写 `revision_date`**，否则会把日期提交进仓库。
- 提交信息不要添加 Co-Authored-By 或任何 Claude 署名。

## 目录结构

```
zensical.toml                 # 全部配置：导航、主题、插件、Markdown 扩展
docs/
  index.md                    # 首页（hero + 三大板块卡片 + 最近更新）
  tags.md                     # 标签索引（<!-- material/tags --> 自动生成）
  research/                   # 科研
    index.md                  #   板块首页：主题卡片
    <topic>/index.md          #   主题首页：文章卡片
    <topic>/<article>.md
  tutorials/                  # 教程（结构同上）
  interests/                  # 兴趣（结构同上）
  about/                      # 关于、写作模板
  stylesheets/extra.css       # 全部自定义样式（配色变量在文件开头）
  javascripts/mathjax.js      # MathJax 配置（ams 编号、\ket 等宏）
  assets/                     # logo.svg / favicon.svg
scripts/site_meta.py          # 生成"最近更新"和 revision_date
inbox/                        # 待整理的原始文件（不会发布；整理完即删除）
```

现有主题：

| 板块 | 主题目录 | 内容 |
|---|---|---|
| 科研 | `research/device-independence/` | 器件无关与网络非局域性 |
| 教程 | —（规划中：量子力学、量子信息基础，只在 `tutorials/index.md` 里以虚线卡片列出） | |
| 兴趣 | `interests/quant-trading/` | 量化交易 |

## 分类规则

| 板块 | 放什么 | 判断标准 |
|---|---|---|
| **科研** `research/` | 量子信息相关的研究推导、论文阅读、研究总结 | 和正在进行的研究直接相关；有"我的项目"、导师讨论、审稿视角 |
| **教程** `tutorials/` | 系统性的课程与学习笔记（量子力学、量子信息基础……） | 教科书式的已知知识，按章节组织，可以独立复习 |
| **兴趣** `interests/` | 学业以外的探索（量化交易，以后还有别的） | 与物理专业无关 |

- 每个板块下按**主题**建子目录，每个主题必须有 `index.md`（主题首页，用卡片列出文章）。
- 拿不准归类时先问作者，不要自行决定。
- 不要创建空页面。规划中的主题只在板块首页用 `fl-planned` 虚线卡片列出，不建页面、不进导航。
- 作者明确不公开的文件不要放进 `docs/`（`docs/` 里的一切都会发布）。

## 新增文章的步骤

1. 文件名用英文或拼音小写加连字符（`self-testing-review.md`），**标题保留中文**，写在第一个 `#` 里；
2. front matter 写 `description`（一句话，用于首页"最近更新"和搜索）和 `tags`；
3. 在 `zensical.toml` 的 `nav` 里加到对应主题下；新主题还要在板块 `index.md` 里加卡片；
4. 在主题 `index.md` 的卡片列表里加一张卡片；
5. 运行 `python scripts/site_meta.py` 刷新首页"最近更新"，再 `zensical build --clean --strict`。

PDF 与介绍页同目录同名（`xxx.md` + `xxx.pdf`），介绍页里写摘要和章节目录（PDF 内容不进搜索），
嵌入代码见 `docs/about/writing-template.md`。按钮和 `<iframe src>` 都直接写文件名，构建时自动换算路径。

## 写作约定

- **公式**：行内 `$...$`，独立 `$$...$$`（单独成段）；编号公式直接写 `\begin{equation}...\end{equation}`
  （外面不套 `$$`），用 `\label{}`/`\eqref{}` 引用。表格里公式中的竖线写 `\vert`，否则会拆开单元格。
  可用宏：`\ket{}`、`\bra{}`、`\braket{}{}`、`\Tr`。
- **提示框**：`!!! 类型 "中文标题"`，`???` 折叠、`???+` 可折叠默认展开。**必须写中文标题**。

  | 类型 | 用途 | 颜色 |
  |---|---|---|
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
- 代码块写语言名（` ```python `），可加 `title="..."`、`linenums="1"`、`hl_lines="2 3"`。

## 标签

尽量复用已有标签，不造近义词。一篇文章 3–6 个标签：**主题标签** + **类型标签**。

| 类别 | 标签 |
|---|---|
| 类型 | `研究推导` `论文阅读` `研究总结` `学习笔记` `PDF` |
| 量子信息 | `器件无关` `Bell 非局域性` `网络非局域性` `自检验` `无信号原理` `纠缠深度` |
| 量化 | `量化交易` `加密货币` `风险管理` `回测` |
| 站务 | `写作模板` `本站` |

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
| 边框、分隔线 | `--fl-border` | `#D9D1BC` | `#2E3832` |

提示框（同一色系、低饱和）：

| 类型 | 变量 | 浅色 | 深色 |
|---|---|---|---|
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
- Logo / favicon（`docs/assets/*.svg`）是墨绿底纸色字，颜色写死在 SVG 里。
- 首页 hero 右侧的 self-testing 公式在 `docs/index.md` 的 `.fl-hero__formula` 里，窄屏时移到介绍下方；
  MathJax 排版完成前公式是收起的（CDN 加载失败时就不显示），避免 LaTeX 源码压住介绍文字。
- 标题：Source Serif 4 + Noto Serif SC（`extra.css` 顶部 `@import`）
- 正文：Noto Sans SC；代码：JetBrains Mono（`zensical.toml` 的 `theme.font`）
- Google Fonts 加载失败时回退到苹方 / 微软雅黑 / 宋体。
- 卡片：圆角 0.8–1rem、1px 细边框、悬停上移 2px 并出现阴影与墨绿边框。

## 已知限制

- Zensical 暂不支持 `git-revision-date` 插件，所以"最后更新"由 `scripts/site_meta.py --stamp` 在 CI 里生成。
- 搜索界面的少量提示文字（如 "Filters"、"results"）目前只有英文，这是 Zensical 新搜索引擎的现状；中文检索本身正常。
- MathJax 与 Mermaid 从 CDN（jsDelivr / unpkg）加载。
