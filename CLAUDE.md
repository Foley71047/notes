# CLAUDE.md —— Foley的笔记

王乐圆（Leyuan Wang，南开大学物理学院，量子信息方向）的个人知识网站。
用 [Zensical](https://zensical.org/docs/) 构建，部署在 <https://foley71047.github.io/notes/>。

## 常用命令

```sh
pip install zensical
python scripts/site_meta.py          # 刷新首页"最近更新"（新增/改名文章后运行并提交）
zensical serve                       # 本地预览（地址见终端输出）
zensical build --clean --strict      # 严格构建：有失效链接或警告即失败（提交前必须通过）
```

- 推送到 `main` 后，`.github/workflows/docs.yml` 自动构建并部署到 GitHub Pages。
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
  | `definition` | 定义 | 灰蓝 |
  | `theorem` / `lemma` / `corollary` / `proposition` | 定理类（正文斜体） | 陶土 |
  | `proof` | 证明（结尾自动加 ∎，通常用 `???` 折叠） | 石灰 |
  | `example` | 例题 | 橄榄绿 |
  | `warning` | 注意 | 琥珀 |
  | `summary` | 总结 | 暗梅 |
  | `note` / `tip` / `danger` | 备注 / 提示 / 危险 | 灰青 / 灰青 / 砖红 |

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

所有颜色是 `docs/stylesheets/extra.css` 开头的 `--fl-*` 变量，其余规则只引用变量。改色只改这里。

| 用途 | 浅色（默认） | 深色 |
|---|---|---|
| 背景 `--fl-bg` | `#FAF9F5` 暖米白 | `#262624` |
| 侧栏/卡片 `--fl-surface` | `#F0EEE6` | `#30302E` |
| 正文 `--fl-text` | `#141413` 深炭 | `#ECEBE4` |
| 次要文字 `--fl-text-2` | `#5E5D59` | `#B7B5AC` |
| 强调 `--fl-accent` | `#D97757` 陶土橙 | `#D97757` |
| 链接 `--fl-link` | `#C15F3C` | `#E8906F` |

- 标题：Source Serif 4 + Noto Serif SC（`extra.css` 顶部 `@import`）
- 正文：Noto Sans SC；代码：JetBrains Mono（`zensical.toml` 的 `theme.font`）
- Google Fonts 加载失败时回退到苹方 / 微软雅黑 / 宋体。
- 卡片：圆角 0.8–1rem、1px 细边框、悬停上移 2px 并出现阴影与陶土色边框。

## 已知限制

- Zensical 暂不支持 `git-revision-date` 插件，所以"最后更新"由 `scripts/site_meta.py --stamp` 在 CI 里生成。
- 搜索界面的少量提示文字（如 "Filters"、"results"）目前只有英文，这是 Zensical 新搜索引擎的现状；中文检索本身正常。
- MathJax 与 Mermaid 从 CDN（jsDelivr / unpkg）加载。
