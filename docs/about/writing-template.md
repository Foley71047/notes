---
description: 本站的写作模板：笔记与概念词条的元数据、要点框、悬停预览、数学公式、提示框、PDF 嵌入、代码块、脚注、选项卡与 Mermaid 图表的写法，复制即可用。
---

# 写作模板

每一节先给出 Markdown 源码，下面紧跟渲染效果。写新文章时，复制对应片段即可。
{ .page-lead }

## 网站结构

| 目录 | 放什么 | 列表怎么来 |
|---|---|---|
| `docs/notes/` | 笔记：思考、论文阅读、有的没的 | [笔记](../notes/index.md)页自动列出，按更新时间倒序 |
| `docs/concepts/` | 概念词条：一个定理、不等式、结论或基本概念 | [概念](../concepts/index.md)页自动列出，按英文名首字母排序 |
| `docs/about/` | 关于、写作模板 | — |

新建文件后**不需要改导航或任何列表**：笔记列表、概念速查表、[标签](../tags.md)页、首页"最近更新"和"引用本概念的笔记"都在构建时根据元数据自动生成。页面上的信息栏（类型、更新日期、前置知识）也全部来自元数据，正文里不用写。

## 新建一篇笔记

1. 在 `docs/notes/` 下新建文件，**文件名用英文或拼音**，例如 `docs/notes/self-testing-review.md`；图片放在 `docs/notes/images/` 下；
2. 开头写 front matter，标题写在第一个一级标题里（保留中文）；
3. 推送到 GitHub，网站会自动更新。

```markdown title="笔记开头"
---
description: 一句话摘要，显示在笔记列表、首页"最近更新"和搜索结果里。
type: 论文阅读
tags:
  - 器件无关
  - 纠缠
prerequisites:                        # 可选
  - ../concepts/chsh-inequality.md    # 站内页面：写相对路径，显示为该页标题的链接
  - 线性代数                           # 其他：原样显示
---

# 自检验综述阅读笔记

一句话副标题（可选）
{ .page-lead }
```

| 字段 | 必填 | 可选值 / 写法 | 显示在哪里 |
|---|---|---|---|
| `description` | 是 | 一句话 | 笔记列表、首页"最近更新"、搜索结果 |
| `type` | 是 | `思考` / `论文阅读` / `有的没的` | 信息栏、笔记列表、筛选按钮 |
| `tags` | 是 | 2–4 个，只能用[标签清单](#标签)里的 | 笔记列表、页面底部、标签页 |
| `prerequisites` | 否 | 列表；站内页面写相对 `.md` 路径，其他写文字 | 信息栏"前置知识" |

更新日期取自 git 最后一次提交，不用手写。

### 类型怎么选

| 类型 | 写什么 | 例子 |
|---|---|---|
| **思考** | 自己的推导、研究总结和想法 | 项目推导、组会后的整理 |
| **论文阅读** | 一篇论文的问题、方法、结论与疑问 | 某篇 PRL 的阅读笔记 |
| **有的没的** | 学业以外的内容和零散杂记 | 量化交易 |

### 要点框

长笔记可以在开头（副标题之后）放一个"要点"框，用三五条列出全文结论，读者先看这里就知道值不值得往下读。

```markdown title="要点框写法"
!!! keypoints "要点"
    - DI 的结论只依赖概率表 $P$，但几乎总是关于设备内部的结论。
    - 无信号原理推不出源独立，网络场景要单独假设。
    - self-testing 只能确定到局域等距变换的精度。
```

!!! keypoints "要点"
    - DI 的结论只依赖概率表 $P$，但几乎总是关于设备内部的结论。
    - 无信号原理推不出源独立，网络场景要单独假设。
    - self-testing 只能确定到局域等距变换的精度。

## 新建一个概念词条

每个词条是一个**定理、不等式、结论**（比如"CHSH 不等式""Tsirelson 界"），或者一个**基本概念**（比如"纠缠熵""POVM"）。概念词条可以和同名标签并存：标签用来归类，词条用来解释。

在 `docs/concepts/` 下新建文件（如 `docs/concepts/tsirelson-bound.md`），按下面两种结构之一写。标题下的英文名和标签、文末的"引用本概念的笔记"都会自动生成，不要自己写。

=== "定理类"

    ````markdown
    ---
    en: Tsirelson's bound                              # 英文名
    statement: '量子力学中 CHSH 值满足 $\lvert S\rvert\le 2\sqrt2$'   # 简介，显示在速查表里
    description: 一句话说明，用于搜索结果。
    tags:
      - Bell 非局域性
      - 半定规划
    ---

    # Tsirelson 界

    !!! theorem "陈述"
        完整、精确的陈述（悬停预览显示的就是这一框）。

    ## 直观含义

    ## 成立条件

    ## 证明思路

    ## 何时取等

    ## 相关结果
    ````

=== "概念类"

    ````markdown
    ---
    en: positive operator-valued measure (POVM)
    statement: '一组半正定算符 $\{E_i\}$，满足 $\sum_i E_i=\mathbb 1$'
    description: 一句话说明，用于搜索结果。
    tags:
      - 量子测量
    ---

    # POVM

    !!! definition "定义"
        严格定义（悬停预览显示的就是这一框）。

    ## 直观含义

    ## 例子

    ## 相关结果
    ````

!!! tip "简介（statement）里的公式"
    `statement` 支持 `$...$` 公式和 `**加粗**`。整行用单引号括起来（`'...'`），里面的反斜杠照写；不要用双引号，否则反斜杠要写两遍。

### 悬停预览

在任何页面里链接到概念词条，鼠标悬停在链接上就会弹出预览卡片，显示词条的英文名、标签和第一个框（"陈述"或"定义"，公式也会排版）：

```markdown title="链接到概念"
量子力学允许的最大值由 [Tsirelson 界](../concepts/tsirelson-bound.md) 给出。
```

量子力学允许的最大值由 [Tsirelson 界](../concepts/tsirelson-bound.md) 给出；局域模型的上界见 [CHSH 不等式](../concepts/chsh-inequality.md)。（把鼠标放到这两个链接上试试。）

这是 Zensical 的"即时预览"功能（`zensical.toml` 里的 `zensical.extensions.preview`），对所有指向 `docs/concepts/` 的站内链接自动生效。只有**写成链接**的名字才有预览；手机上长按链接也能看到。同时，笔记里链接过的词条，会自动出现在该词条末尾的"引用本概念的笔记"里。

## 标签

标签只表示**主题或方法**，不表示类型（类型用 `type`）或进度。一篇笔记 2–4 个，只能从下面的清单里选：

| 类别 | 标签 |
|---|---|
| 主题 | `纠缠` `Bell 非局域性` `导引` `器件无关` `相干性` `资源理论` `量子测量` `量子态层析` `线性光学` |
| 方法 | `数值优化` `半定规划` |
| 兴趣 | `量化` |

需要新标签时，先把它加进 `zensical.toml` 的 `[project.extra.tag_groups]`（并同步 `CLAUDE.md`），再在文章里使用。运行 `python scripts/site_data.py` 可以检查所有文章的类型和标签是否合规。

## 数学公式

行内公式用 `$...$`，独立公式用 `$$...$$`（单独成段）。需要编号的公式直接写 `\begin{equation}...\end{equation}`（或 `align`，**外面不要再套 `$$`**），配合 `\label` 和 `\eqref` 引用；`$$...$$` 里的公式不编号。

```latex title="公式写法"
Bell 态 $\ket{\Phi^+}=\frac{1}{\sqrt2}(\ket{00}+\ket{11})$ 的约化态是最大混态。

$$
\rho_A=\Tr_B\ket{\Phi^+}\bra{\Phi^+}=\frac{\mathbb 1}{2}
$$

\begin{equation}
  S=\langle A_0B_0\rangle+\langle A_0B_1\rangle+\langle A_1B_0\rangle-\langle A_1B_1\rangle\le 2
  \label{eq:chsh}
\end{equation}

量子力学允许的最大值是 $2\sqrt2$，即式 $\eqref{eq:chsh}$ 的 Tsirelson 界。

\begin{align}
  p(ab|xy) &= \Tr\big[\rho\,(M_{a|x}\otimes N_{b|y})\big] \label{eq:born}\\
  \sum_b p(ab|xy) &= \Tr\big[\rho\,(M_{a|x}\otimes\mathbb 1)\big]
\end{align}
```

Bell 态 $\ket{\Phi^+}=\frac{1}{\sqrt2}(\ket{00}+\ket{11})$ 的约化态是最大混态。

$$
\rho_A=\Tr_B\ket{\Phi^+}\bra{\Phi^+}=\frac{\mathbb 1}{2}
$$

\begin{equation}
  S=\langle A_0B_0\rangle+\langle A_0B_1\rangle+\langle A_1B_0\rangle-\langle A_1B_1\rangle\le 2
  \label{eq:chsh}
\end{equation}

量子力学允许的最大值是 $2\sqrt2$，即式 $\eqref{eq:chsh}$ 的 Tsirelson 界。

\begin{align}
  p(ab|xy) &= \Tr\big[\rho\,(M_{a|x}\otimes N_{b|y})\big] \label{eq:born}\\
  \sum_b p(ab|xy) &= \Tr\big[\rho\,(M_{a|x}\otimes\mathbb 1)\big]
\end{align}

!!! tip "预定义的宏"
    `\ket{ψ}`、`\bra{ψ}`、`\braket{φ}{ψ}`、`\Tr` 已经在 `docs/javascripts/mathjax.js` 里定义好，可以直接用。表格里的竖线请写成 `\vert` 或 `\mid`，否则会被当成表格分隔符。

## 提示框

六种学术提示框，颜色各不相同。`!!!` 是展开的，`???` 是默认折叠的，`???+` 是可折叠但默认展开。**标题请始终写上**（写在引号里），否则会显示英文类型名。

````markdown title="提示框写法"
!!! definition "定义 1（$k$-producible）"
    一个 $n$ 体纯态称为 $k$-producible，如果它能写成若干个至多 $k$ 体的纯态的张量积。

!!! theorem "定理 2（Tsirelson 界）"
    对任意量子态和二值观测量，CHSH 表达式满足 $S\le 2\sqrt2$。

??? proof "证明"
    令 $\mathcal B=A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1)$，
    计算 $\mathcal B^2$ 并用算符范数估计即得。

!!! example "例题 3"
    计算 $\ket{\Phi^+}$ 在最优测量下的 CHSH 值。

!!! warning "注意"
    违背 Bell 不等式只证明了不可分，不能说明态就是 $\ket{\Phi^+}$。

???+ summary "总结"
    DI 结论只依赖概率表 $P$，但几乎总是关于设备内部的结论。
````

!!! definition "定义 1（$k$-producible）"
    一个 $n$ 体纯态称为 $k$-producible，如果它能写成若干个至多 $k$ 体的纯态的张量积。

!!! theorem "定理 2（Tsirelson 界）"
    对任意量子态和二值观测量，CHSH 表达式满足 $S\le 2\sqrt2$。

??? proof "证明"
    令 $\mathcal B=A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1)$，
    计算 $\mathcal B^2$ 并用算符范数估计即得。

!!! example "例题 3"
    计算 $\ket{\Phi^+}$ 在最优测量下的 CHSH 值。

!!! warning "注意"
    违背 Bell 不等式只证明了不可分，不能说明态就是 $\ket{\Phi^+}$。

???+ summary "总结"
    DI 结论只依赖概率表 $P$，但几乎总是关于设备内部的结论。

此外还可以用 `lemma`、`corollary`、`proposition`（与定理同色）、`keypoints`（要点，见上文）、`note`、`tip`、`danger` 等类型。

## PDF 嵌入

PDF 和它的介绍页放在同一个目录（`docs/notes/`）、用同一个英文文件名，例如 `crypto-quant-trading.md` 和 `crypto-quant-trading.pdf`。下面这段会生成"桌面端内嵌阅读 + 下载按钮"，手机上自动隐藏阅读框、只保留按钮。

!!! tip "路径怎么写"
    按钮链接和 `<iframe>` 的 `src` 都**直接写 PDF 文件名**（相对于当前 `.md` 文件），构建时会自动换算成网页上的正确路径。

```html title="PDF 嵌入写法"
<div class="fl-pdf" markdown>
<div class="fl-pdf__bar" markdown>
<p class="fl-pdf__name" markdown="span">:lucide-file-text: 文件标题 <small>PDF · 20 页</small></p>
<p class="fl-pdf__actions" markdown>[:lucide-external-link: 新标签打开](my-notes.pdf){ .md-button target="_blank" rel="noopener" } [:lucide-download: 下载 PDF](my-notes.pdf){ .md-button .md-button--primary download }</p>
</div>
<iframe class="fl-pdf__frame" src="my-notes.pdf#view=FitH" title="文件标题" loading="lazy"></iframe>
<p class="fl-pdf__mobile">手机浏览器对内嵌 PDF 的支持有限，建议下载或在新标签页中打开。</p>
</div>
```

实际效果见 [加密货币交易：从零到量化](../notes/crypto-quant-trading.md)。PDF 里的文字不会进入站内搜索，所以介绍页里最好写上摘要和章节目录。

## 代码块

代码块右上角自带一键复制。可以加标题、行号和高亮行：

````markdown title="代码块写法"
```python title="kelly.py" linenums="1" hl_lines="4 5"
def kelly_fraction(p: float, b: float) -> float:
    """胜率 p、赔率 b 时的 Kelly 最优仓位比例。"""
    q = 1 - p
    f = (b * p - q) / b
    return max(f, 0.0)
```
````

```python title="kelly.py" linenums="1" hl_lines="4 5"
def kelly_fraction(p: float, b: float) -> float:
    """胜率 p、赔率 b 时的 Kelly 最优仓位比例。"""
    q = 1 - p
    f = (b * p - q) / b
    return max(f, 0.0)
```

行内代码高亮：`#!python print("hello")`。

## 脚注

```markdown title="脚注写法"
CHSH 不等式最早由 Clauser 等人提出[^chsh]。

[^chsh]: J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, *PRL* **23**, 880 (1969).
```

CHSH 不等式最早由 Clauser 等人提出[^chsh]。鼠标悬停在脚注编号上可以直接预览。

[^chsh]: J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, *PRL* **23**, 880 (1969).

## 内容选项卡

```markdown title="选项卡写法"
=== "Python"

    ```python
    import numpy as np
    returns = np.diff(np.log(prices))
    ```

=== "公式"

    $$r_t=\ln P_t-\ln P_{t-1}$$
```

=== "Python"

    ```python
    import numpy as np
    returns = np.diff(np.log(prices))
    ```

=== "公式"

    $$r_t=\ln P_t-\ln P_{t-1}$$

## Mermaid 图表

````markdown title="Mermaid 写法"
```mermaid
flowchart LR
  A[要认证的性质] --> B{坏集合是凸的吗?}
  B -- 是 --> C[源之间无量子关联即可]
  B -- 否 --> D[必须假设源完全独立]
```
````

```mermaid
flowchart LR
  A[要认证的性质] --> B{坏集合是凸的吗?}
  B -- 是 --> C[源之间无量子关联即可]
  B -- 否 --> D[必须假设源完全独立]
```

## 其他常用写法

| 效果 | 写法 |
|---|---|
| ==高亮== | `==高亮==` |
| ~~删除线~~ | `~~删除线~~` |
| 上标 x^2^、下标 H~2~O | `x^2^`、`H~2~O` |
| 按键 ++ctrl+c++ | `++ctrl+c++` |
| 图标 :lucide-atom: | `:lucide-atom:` |
| 站内链接 | `[标签索引](../tags.md)`（写 `.md` 相对路径，构建时会检查是否失效） |
| 图片 | `![说明](images/fig1.png)`，图片放在文章同目录的 `images/` 下 |

- [x] 任务列表
- [ ] 也可以用
