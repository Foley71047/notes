# 器件无关（DI）到底在讲什么
### ——一份从假设记账出发的梳理，配你自己的项目做例子

---

## 0. 先诊断：你说的"隔阂"来自哪几块知识

你现在的理解是「DI 就是不信任设备、只看概率输出能得到什么结论」。**这句话是对的，但它是结论，不是操作手册。** 你卡住的地方，都在这句话没展开的部分：

| 你的困惑 | 背后缺的那块知识 | 本文对应章节 |
|---|---|---|
| "不相信他的什么？具体不信任什么？" | **假设记账（assumption bookkeeping）**：DI 不是"零假设"，而是一张明确的清单：哪些必须假设、哪些被扔掉 | §2、§3 |
| "所以我们要怎么设计实验？" | **DI 结论的逻辑形式**是"对一切能重现该统计的量子实现"，因此实验设计=构造一个泛函 + 证一条不等式 | §4、§5 |
| "什么诚实方，看不明白" | **DI 源于密码学**，天生是"验证者 vs 对手"的博弈；"诚实实现"是可行性分析用的参照物 | §4 |
| "self-testing 是得到完整形式" | **等价类**：概率统计对局域幺正、附加 junk、复共轭都不变，所以"完整"只能到这个精度 | §6 |
| （隐含）我的方案到底算不算 DI | **半 DI 谱系**：DI / 网络 DI / 1SDI / MDI / 维数受限是五个不同的格子 | §7 |
| 上一轮你问的"源可以任意吗" | **soundness vs completeness** 没分开 | §4.3 |

后面按这个顺序讲。每节末尾用**你自己的项目**做例子。

---

## 1. 基本图像：把实验换成一张概率表

### 1.1 黑盒
DI 的第一步是**把实验室里的设备换成一个黑盒**：它有一个输入口（你按按钮 $x$）和一个输出口（它吐出结果 $a$）。你不许打开它，不许问里面是什么晶体、什么激光、什么探测器，甚至不许假设它的希尔伯特空间是几维。

$n$ 个这样的盒子放在 $n$ 个分开的实验室里，实验的**全部**可观测内容就是一张表：

$$P=\{\,p(a_1\cdots a_n\,|\,x_1\cdots x_n)\,\}.$$

这张表叫 **behaviour / correlation / 关联**。DI 的世界里，**除了这张表，什么都不存在。**

### 1.2 DI 结论的定义
> **一个结论是 DI 的，当且仅当它只依赖 $P$，而不依赖任何关于设备内部的额外信息。**

这里有个容易忽略的要点：DI 结论**几乎总是关于"设备内部"的**（比如"这个态是纠缠的"），但**推导只用了 $P$**。这不矛盾——因为量子力学限制了什么样的内部结构能产生什么样的 $P$。

### 1.3 一个日常类比
你买了一台自动售货机，声称"里面有一个真随机数发生器"。你不能拆机。你能做的只有：投币、按不同的按钮、记录出货。DI 问的是：**存不存在一种输入-输出统计，使得"里面没有真随机数发生器"这件事在逻辑上被排除？** Bell 定理说：有。

---

## 2. 关键的思维翻转：从"我的设备是什么"改成"什么设备能产生这张表"

这是最重要的一次视角切换，也是最多人卡住的地方。

**器件相关（device-dependent）的问法**：
> 我有一个态 $\rho$ 和一组测量 $\{M_{a|x}\}$，它们产生什么统计？（正问题）

**DI 的问法**：
> 我观测到了统计 $P$。**所有**能产生 $P$ 的量子实现 $(\mathcal H,\rho,\{M_{a|x}\})$ 组成一个集合 $\mathcal S(P)$。这个集合里的成员**共同具有**什么性质？（反问题，且是"对全称量词"的）

于是 DI 定理的标准句式永远是：

$$\forall\,(\mathcal H,\rho,\{M\})\in\mathcal S(P):\quad \text{性质 } X \text{ 成立}.$$

**推论 1：DI 结论天然是"否定式/下界式"的。** 你能证的是"$\rho$ **不可能**可分""维数**至少**是 4""随机数**至少**有 $r$ 比特""纠缠深度**至少**是 $k+1$"。你几乎永远不能 DI 地说"$\rho$ 恰好等于某某"——除非 $\mathcal S(P)$ 塌缩成一个等价类，那就是 self-testing（§6）。

**推论 2：设计 DI 判据 = 找一个对整个"坏集合"都成立的不等式。** 具体见 §5。

> **对你的项目**：你的 $J_c\le 0$ 就是这个句式。完整写法是：
> "在假设【源之间无量子关联】下，对一切能产生观测数据 $p(\vec a,c|\vec x)$ 的量子实现，只要中心 effect $M_c$ 关于划分 $C_1|\cdots|C_n$ 是 $k$-producible，就有 $J_c\le0$。"
> 于是观测到 $J_c>0$ ⟹ 排除了所有 $k$-producible 的实现 ⟹ 深度 $\ge k+1$。

---

## 3. 假设记账：DI 到底不信任什么、又必须信任什么 ★

**"DI = 无假设"是最常见的误解。** DI 只是把假设清单压到很短，但清单非空，而且每一条都对应一个真实的实验漏洞。

### 3.1 必须保留的假设（DI 也删不掉）

| 编号 | 假设 | 说明 | 违反它 = 什么漏洞 |
|---|---|---|---|
| **A1** | 量子力学成立（或退一步：no-signalling） | 你要用 Born 规则和张量积结构写下 $\mathcal S(P)$ | — |
| **A2** | 实验室分离、不通信 | 盒子 $i$ 的输出不能依赖盒子 $j$ 的输入 | **locality loophole**（定域性漏洞） |
| **A3** | 输入是自由选择的，与设备内部状态独立 | 设备不能"预知"你要按哪个键 | **freedom-of-choice / measurement-independence loophole** |
| **A4** | 所有轮次都被记录，不做与输入相关的后选择 | 丢事件必须是与 $x$ 无关的 | **detection loophole**（探测漏洞） |
| **A5** | 统计推断的假设：i.i.d.，或者用鞅/熵累积处理一般情形 | 有限次实验只能给置信区间 | **memory attack**（设备有记忆并跨轮次共谋） |

**这五条是"DI 的最小假设集"。** 你和老师讨论时，如果先把这张表摆出来，很多"隔阂"会当场消失——因为分歧往往是某个人默认了某条、另一个人没默认。

### 3.2 被扔掉的（这才是"不信任设备"的内容）

- ❌ 希尔伯特空间的**维数**（可以是任意大，甚至无穷维）
- ❌ 态是什么（可以是任何 $\rho$，可以带 Eve 的净化）
- ❌ 测量算符是什么（可以是任何 POVM，不必投影，不必是你以为的那个）
- ❌ 设备是否有内部记忆、是否被对手预先编程
- ❌ 不同轮次之间设备的行为是否一致（这条由 A5 的技术手段补上）

**所以"不信任设备"具体的意思是**：在写下 $\mathcal S(P)$ 时，你对 $(\mathcal H,\rho,\{M\})$ **只施加"它们是合法的量子对象"这一个约束**，其余全部放开取遍。

### 3.3 文献例子：三个"loophole-free" Bell 实验
2015 年三个实验第一次同时关掉 A2、A3、A4 三个漏洞，这是理解"DI 的假设是真金白银"的最佳例子：

- 金刚石色心，1.3 km 分离：[Hensen et al., *Nature* **526**, 682 (2015)](https://www.nature.com/articles/nature15759)
- 光子，高探测效率：[Giustina et al., *PRL* **115**, 250401 (2015)](https://link.aps.org/doi/10.1103/PhysRevLett.115.250401)
- 光子，独立随机数源：[Shalm et al., *PRL* **115**, 250402 (2015)](https://link.aps.org/doi/10.1103/PhysRevLett.115.250402)

看它们**为了关掉每一个漏洞分别付出了什么工程代价**，你就会对"DI 的假设清单"有实感：locality 要空间类隔离（距离/时序），detection 要探测效率超过阈值（CHSH 约 82.8%，用 Eberhard 型不等式可降到约 2/3），freedom-of-choice 要独立快速随机数源。

> **对你的项目**：你的场景多一条 A2'——**源之间无量子关联**（§8）。这一条不是从 no-signalling 推出来的，是**额外**假设，必须显式写在定理里。

---

## 4. "验证者 vs 对手"：为什么会冒出"诚实方"这个词 ★

### 4.1 DI 的密码学出身
DI 这个概念是从**密码学**长出来的，不是从基础物理长出来的。原始动机是：Alice 和 Bob 从一个**可能由窃听者 Eve 制造的**设备厂商那里买来盒子，还能不能安全地生成密钥？答案是可以——这就是 DIQKD（[Acín et al., *PRL* **98**, 230501 (2007)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.98.230501)）。

所以 DI 场景里天生有**两个角色**：

- **验证者（verifier / referee）**：只能看到 $P$，要做出判断。就是你，就是实验者。
- **设备 / 对手（device / adversary）**：可以任意选择 $(\mathcal H,\rho,\{M\})$，目标是**让验证者做出错误的肯定判断**。

### 4.2 "诚实实现"（honest implementation）是什么
一个 DI 协议要有用，需要两件事，它们分别对应两个角色：

- **可靠性 / soundness**：*对手骗不过去*。即：任何**不具备**待认证性质的实现，都不能让判据触发。
- **可行性 / completeness**：*诚实厂商造的设备能通过*。即：存在一个按设计做出来的实现（"诚实实现"），它真的具备该性质，并且真的能让判据触发。

**"诚实方 / 诚实实现"就是可行性分析里的那个参照实现。** 它不是一个"人"，是"如果大家都老老实实按理想方案做，会发生什么"的那个设定。

### 4.3 这正好回答你上一轮的疑问 ★
你问："源可以任意吗？不然我发直积态，中心方的纠缠测量对外部方拿到的态就没影响了。"

拆开看：

| | 内容 | 对源的要求 |
|---|---|---|
| **Soundness** | $M_c$ 是 $k$-producible $\Rightarrow J_c\le0$ | **源任意**（只要块间无量子关联） |
| **Completeness** | $M_c$ 深度高 $\Rightarrow$ 真能看到 $J_c>0$ | **源必须够纠缠**，最优是最大纠缠态 |

你说的直积源属于**第二栏**：它让判据测不到东西。但**判据没有出错**——它输出"未检出"，这是正确的输出。

**而 DI 的不对称性正在这里**：DI 要防的是"设备撒谎说自己做了纠缠测量"，不是"设备摆烂让你测不出来"。烂设备只伤害诚实方（白做一场实验），不会让验证者得出错误结论。**所以验证者不需要知道源是什么。**

一句可以记住的话：

> **DI 判据的可靠性对设备的一切选择成立；判据的灵敏度只对好设备成立。这两件事必须分开陈述。**

### 4.4 为什么"对手会用坏源"这个问题本身问错了
对手不会用坏源——坏源对他没好处（触发不了判据）。你要担心的是**对手会不会用某种巧妙的好源 + 低深度测量来伪造违背**。这才是 soundness 要证的东西，而你的引理证的正是这个。

---

## 5. 怎么设计一个 DI 实验：七步配方

这是回答你"所以我们要怎么设计实验"的操作层面。

### 步骤

1. **画因果结构。** 有几个盒子？谁和谁共享源？谁能通信？源之间独立吗？——这一步决定了 $\mathcal S(P)$ 的形状。
2. **写下可观测数据。** 明确 $P$ 里有哪些条目。（注意：只有验证者能同时看到的东西才算，需要事后汇总。）
3. **精确定义要认证的性质 $X$。** 必须是关于 $(\mathcal H,\rho,\{M\})$ 的数学陈述，且**对等价类不变**（见 §6.3）。
4. **构造泛函 $W[P]$，证 soundness**：$\forall$ 不具备 $X$ 的量子实现，$W[P]\le0$。
   - 这一步是全部的技术含量。常用工具：Bell 不等式的 SOS 分解、NPA 层级（[Navascués-Pironio-Acín, *PRL* **98**, 010401 (2007)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.98.010401)）、对偶性、以及你用的那种"结构分解 + 每块单独取最优"的组合论证。
5. **给出诚实实现，证 completeness**：写下一个具体的 $(\rho^\star,M^\star)$ 使 $W>0$，最好还能算出最大值。
6. **噪声/鲁棒性分析**：把可见度 $\eta,v$ 之类的参数放进诚实实现，求 $W>0$ 的阈值。
7. **有限统计**：从有限轮次的频率到 $P$ 的置信区间；若不假设 i.i.d.，需要鞅不等式或熵累积定理。

### 用你的项目逐条对照

| 步骤 | 你的方案 | 状态 |
|---|---|---|
| 1 因果结构 | $n$ 个源的星型网络，$n$ 个外部方 + 中心方，源独立 | ✅ |
| 2 数据 | $p(\vec a,c\,|\,\vec x)$，含 $p(c)$ | ✅ |
| 3 性质 | $M_c$ 关于 $C_1\vert\cdots\vert C_n$ **不是** $k$-producible | ✅（但要注意 §6.3 的不变性，见下） |
| 4 soundness | 交换引理 + 态的深度 Bell 界 $S^{Q,*}_k$ | ✅（$\zeta>0$ 的洞待补） |
| 5 completeness | GHZ projector + $X$–$Y$ 平面 ansatz，达到 $S^{Q,*}_n$ | ✅ |
| 6 鲁棒性 | 白噪声/彩噪声阈值 | ✅（$n=2$ colored 那处要修） |
| 7 有限统计 | — | ❌ **还没做**，投稿前至少要有一段 |

**注意步骤 3 的不变性检查**：$k$-producibility 在局域幺正、附加 ancilla（$\otimes\mathbb 1$）、整体转置、复共轭下都不变。**这是你的性质"可以被 DI 认证"的前提**，值得单独写一句——很多性质（比如"这个态的保真度是 0.9"）不满足，就不可能 DI 认证。

---

## 6. Self-testing：DI 的最强形式，以及"完整"到底完整到什么程度

### 6.1 什么时候 $\mathcal S(P)$ 会塌缩
一般来说，能产生 $P$ 的实现有无穷多个。但对某些特殊的 $P$（典型是 Bell 不等式的**最大**违背点），$\mathcal S(P)$ 会塌缩成**一个等价类**。这时你就从"性质认证"升级成了"完全刻画"，这就是 self-testing。

起源：[Mayers & Yao (1998/2004)](https://arxiv.org/abs/quant-ph/0307205)。综述（**强烈建议你完整读一遍**）：[Šupić & Bowles, *Self-testing of quantum systems: a review*, Quantum **4**, 337 (2020)](https://quantum-journal.org/papers/q-2020-09-30-337/)（[arXiv:1904.10042](https://arxiv.org/abs/1904.10042)）。

### 6.2 为什么只能到"等价类"——三个删不掉的自由度
概率 $p(\vec a|\vec x)=\mathrm{Tr}[\rho\bigotimes M_{a_i|x_i}]$ 对下面三种改动**完全不变**，所以统计原理上无法区分它们：

1. **局域幺正**：$\rho\to U\rho U^\dagger$，$M\to UMU^\dagger$（$U=\bigotimes_i U_i$）。
2. **附加 junk**：$\rho\to\rho\otimes\xi$，$M\to M\otimes\mathbb 1$。设备完全可以在旁边多带一堆没用的自由度。
3. **整体复共轭**：$\rho\to\rho^*$，$M\to M^*$（在实数基下）。因为迹是实的。

因此 self-testing 的标准结论长这样：**存在局域等距同构（isometry）$\Phi=\bigotimes_i\Phi_i$，使得**

$$\Phi(\rho)=|\psi^\star\rangle\langle\psi^\star|\otimes\xi,\qquad \Phi(M_{a|x}\,\cdot\,)=M^\star_{a|x}\otimes\mathbb 1(\cdot),$$

**或其复共轭。** 所以"得到完整形式"要理解成：**在这个等价类的意义下完整**。它不是"我知道了那个态的每个矩阵元"，而是"任何实现都必须包含那个态作为一个可提取的子系统"。

> 这条也解释了 Sarkar 那篇 Nat. Phys. 为什么反复写 "up to complex conjugation"。

### 6.3 一个必须做的检查
既然只能到等价类，**你要认证的性质必须对这三种改动不变**，否则问题本身就不良定义。
- $k$-producibility：局域幺正 ✅、$\otimes\mathbb 1$ ✅、复共轭 ✅ → **可以 DI 认证**。
- "态的纠缠熵" ✅；"态在计算基下的第 3 个矩阵元" ❌；"测量是投影的" ❌（附加 junk 会破坏）。

### 6.4 rigidity 与鲁棒性
理想 self-testing 是"$P=P^\star\Rightarrow$ 等价"。实验里只能有 "$P$ 与 $P^\star$ 相差 $\epsilon$"，于是需要 **robust self-testing**：结论变成"距离 $\le f(\epsilon)$"。$f$ 通常是 $O(\sqrt\epsilon)$ 量级，常数还可能随方数快速变大——**这就是我上一轮说"串联自检会让鲁棒性塌方"的意思**。经典例子：[McKague, Yang, Scarani, *J. Phys. A* **45**, 455304 (2012)](https://arxiv.org/abs/1203.2976)（单态的鲁棒自检）。

### 6.5 self-testing 的两个"最强"结果，可以当参照系
- 网络里可以自检**任意纠缠态**：[Šupić, Bowles, Renou, Acín, Hoban, *Nature Physics* **19**, 670 (2023)](https://www.nature.com/articles/s41567-023-01945-4)
- 网络里可以自检**任意态或任意测量**（你手上那篇）：[Sarkar, Orthey, Augusiak, *Nature Physics* (2026)](https://doi.org/10.1038/s41567-026-03181-y)
- 自检**纠缠测量**的起点：[Renou et al., *PRL* **121**, 250507 (2018)] 与 [Bancal, Sangouard, Sekatski, *PRL* **121**, 250506 (2018)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.121.250506)

---

## 7. 半 DI 谱系：你的方案站在哪一格 ★

这是消除你和老师"隔阂"最有用的一张表。**每一格的区别只有一件事：你信任什么。**

| 格 | 信任什么 | 不信任什么 | 代表文献 |
|---|---|---|---|
| **完全器件相关**（层析） | 全部测量、全部制备 | — | 标准 state tomography |
| **维数受限半 DI** | 只信任希尔伯特空间维数上界 | 态、测量 | [Gallego et al., *PRL* **105**, 230501 (2010)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.105.230501)；[Pawłowski & Brunner, *PRA* **84**, 010302(R) (2011)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.84.010302)；**Tavakoli et al. [arXiv:1805.00377]**（认证纠缠测量） |
| **MDI / semi-quantum** | 信任**制备**（送进去的量子态已知） | 测量设备完全不信任 | [Buscemi, *PRL* **108**, 200401 (2012)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.108.200401)；[Branciard, Rosset, Liang, Gisin, *PRL* **110**, 060405 (2013)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.110.060405)；[Zhao-Yuan-Ma, arXiv:1607.08002](https://ar5iv.arxiv.org/html/1607.08002) |
| **单边 DI（steering）** | 信任一方的测量 | 另一方全部 | [Wiseman, Jones, Doherty, *PRL* **98**, 140402 (2007)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.98.140402) |
| **网络 DI** | 只信任**因果结构**（源独立） | 态、测量、维数全部 | [Branciard, Gisin, Pironio, *PRL* **104**, 170401 (2010)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.170401)；[Branciard et al., *PRA* **85**, 032119 (2012)](https://link.aps.org/doi/10.1103/PhysRevA.85.032119) |
| **全 DI（标准 Bell）** | 只信任 §3.1 那五条 | 一切 | Bell 1964；CHSH 1969；[Brunner et al., *RMP* **86**, 419 (2014)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.86.419) |

> **你的文档横跨两格，这一点必须在文章里写清楚，否则审稿人第一句就会问：**
> - §1–§5（$\rho^{(i)}_{a|x}$ 被信任、$D^{(i)}_x$ 已知）→ **MDI 格**
> - §6（只用源独立性）→ **网络 DI 格**
>
> 而且它们不是"同一个结果的两种写法"，是**两个强度不同的定理**。建议在文章里做成一个 assumption ladder：MDI 版本给出直观和紧性，网络 DI 版本给出最强结论。

---

## 8. 网络 DI 的特殊之处（你的场景）

标准 Bell 场景只有一个源，网络场景有多个独立源，这带来三个新东西：

### 8.1 源独立性是**新的假设**
它不能从 no-signalling 推出来。它是对因果结构的假设，地位类似 §3.1 的 A2。**没有它，你的判据会出假阳性**：
> 反例：让 $A_1,A_2$ 直接共享一个 $|\Phi^+\rangle$（源之间有量子关联），中心方只做乘积测量 $M_c=|0\rangle\langle0|\otimes|0\rangle\langle0|$。后选择态仍是 $|\Phi^+\rangle_{A_1A_2}$，CHSH 违背，$J_c>0$——但 $M_c$ 是 1-producible。

**好消息**：经典关联的源不会出问题（对每个隐变量 $\mu$ 用引理，再用 $k$-producible 集合的凸性）。所以准确的假设是「**源之间无量子关联**」，比「源独立」弱，值得写成一条 Remark。

### 8.2 网络关联集合是**非凸**的
因为 $\rho=\bigotimes_i\rho_i$ 这个约束不是凸的（两个乘积态的混合一般不是乘积态）。后果：
- 局域界不再是简单的线性规划；
- NPA 层级不能直接用，需要 **inflation** 或 scalar extension 之类的技术（[Wolfe, Spekkens, Fritz, *J. Causal Inference* **7**, 20170020 (2019)](https://arxiv.org/abs/1609.00672)）。

**但你的判据绕开了这个麻烦**：你不需要刻画网络关联集合，你只需要"交换后的态是 $k$-producible"+"$k$-producible 态的 Bell 界"，后者是标准的凸问题。**这是你方案的一个技术优点，值得说出来。**

### 8.3 后选择
网络判据几乎都要在中心方的某个输出 $c$ 上后选择。合法性来自 no-signalling：$p(c|\vec x)=p(c)$ 与 $\vec x$ 无关。写成 $J_c$ 那种"乘回 $p(c)$"的线性形式后，判据是原始概率的线性泛函，完全没有 fair-sampling 问题。可引：[Orsucci, Bancal, Sangouard, Sekatski, *Quantum* **4**, 238 (2020)](https://quantum-journal.org/papers/q-2020-03-02-238/)。

---

## 9. 常见误解快问快答

**Q：DI 是不是就是"没有任何假设"？**
不是。是 §3.1 那五条 + 场景特有的因果假设。DI 的价值在于**假设很少且都可实验检验**，不在于"零假设"。

**Q：违背了 Bell 不等式，是不是就证明了态是 $|\Phi^+\rangle$？**
不是。只证明了"不可分"。要说是 $|\Phi^+\rangle$，需要**最大**违背（或接近最大），且结论只到等价类。

**Q：不假设维数，那不是要处理无穷维吗？**
是，但通常不需要显式处理。要么用代数方法（只用算符关系，不用矩阵表示），要么用 NPA 这种对维数不敏感的松弛，要么用 Jordan 引理把二值观测量约化成 qubit 直和。

**Q：我的判据没测出来，是不是判据不好？**
先分清是 soundness 还是 completeness 的问题。判据没触发只说明"在这个噪声水平下这个实现测不出来"，不代表判据错。

**Q：DI 结论能不能是"这个测量恰好是 GHZ 基"？**
可以，但那要 self-testing 级别的条件（最大违背 / 一整套关联条件），而且只到等价类。**深度下界要弱得多、也鲁棒得多**——这正是你的判据相对 Sarkar 完全自检方案的优势。

**Q：DI 在实验上真做得出来吗？**
做得出来，但很贵。参考 2022 年的两个 DIQKD 实验：[Nadlinger et al., *Nature* **607**, 682 (2022)](https://www.nature.com/articles/s41586-022-04941-5)（囚禁离子）和 [Zhang et al., *Nature* **607**, 687 (2022)](https://www.nature.com/articles/s41586-022-04891-y)（光子）。看它们的码率和实验规模，你会对"DI 的代价"有实感。

---

## 10. 和老师沟通时的共同语言

每次讨论前，把结论写成这个固定模板，隔阂会少一大半：

> **在假设 {A1,…,A5, 源之间无量子关联} 下，对一切能重现观测数据 $P$ 的量子实现，若 $M_c$ 是 $k$-producible，则 $J_c\le0$。**

三个必答问题，任何 DI 讨论都可以用它们定位：

1. **你信任什么？**（定位到 §7 的哪一格）
2. **你证的是 soundness 还是 completeness？**（§4.2）
3. **你的结论是"对一切实现"还是"对某个实现"？**（全称还是存在）

你上一轮的困惑正好是第 2 问没分开；你和老师关于"要不要接 self-testing"的分歧，本质是第 1 问没对齐——**他想的是"完全刻画"（需要自检），你需要的是"深度下界"（不需要）。** 两个人说的都对，只是目标不同。

---

## 11. 建议的阅读顺序

1. **[Brunner et al., *Bell nonlocality*, RMP 86, 419 (2014)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.86.419)** — 第 I–III 章 + 漏洞那一节。先建立 §1–§3 的图像。
2. **[Šupić & Bowles, *Self-testing: a review*, Quantum 4, 337 (2020)](https://quantum-journal.org/papers/q-2020-09-30-337/)** — 第 2 章（定义与等价类）必读，能一次解决你对"完整形式"的困惑。
3. **[Branciard, Gisin, Pironio, PRL 104, 170401 (2010)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.170401)** + [PRA 85, 032119 (2012)](https://link.aps.org/doi/10.1103/PhysRevA.85.032119) — 网络 DI 的入门，理解"源独立"为什么是新假设。
4. **[Buscemi, PRL 108, 200401 (2012)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.108.200401)** — 搞清 MDI 到底信任什么，对应你 §1–§5。
5. **[Sarkar, arXiv:2502.06986](https://arxiv.org/html/2502.06986)** — 你的直接前作，重点看他怎么写"信任态、不信任测量"和星型网络那一节的逻辑结构。
6. 需要做步骤 7（有限统计）时再看熵累积定理相关文献。

---

## Sources

- [Brunner, Cavalcanti, Pironio, Scarani, Wehner, *Bell nonlocality*, Rev. Mod. Phys. 86, 419 (2014)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.86.419)
- [Šupić & Bowles, *Self-testing of quantum systems: a review*, Quantum 4, 337 (2020)](https://quantum-journal.org/papers/q-2020-09-30-337/)｜[arXiv:1904.10042](https://arxiv.org/abs/1904.10042)
- [Hensen et al., Nature 526, 682 (2015)](https://www.nature.com/articles/nature15759)
- [Giustina et al., PRL 115, 250401 (2015)](https://link.aps.org/doi/10.1103/PhysRevLett.115.250401)
- [Shalm et al., PRL 115, 250402 (2015)](https://link.aps.org/doi/10.1103/PhysRevLett.115.250402)
- [Nadlinger et al., Nature 607, 682 (2022)](https://www.nature.com/articles/s41586-022-04941-5)
- [Zhang et al., Nature 607, 687 (2022)](https://www.nature.com/articles/s41586-022-04891-y)
- [Branciard, Gisin, Pironio, PRL 104, 170401 (2010)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.170401)
- [Branciard, Rosset, Gisin, Pironio, PRA 85, 032119 (2012)](https://link.aps.org/doi/10.1103/PhysRevA.85.032119)
- [Wolfe, Spekkens, Fritz, inflation technique, arXiv:1609.00672](https://arxiv.org/abs/1609.00672)
- [Orsucci, Bancal, Sangouard, Sekatski, Quantum 4, 238 (2020)](https://quantum-journal.org/papers/q-2020-03-02-238/)
- [Bancal, Sangouard, Sekatski, PRL 121, 250506 (2018)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.121.250506)
- [Šupić, Bowles, Renou, Acín, Hoban, Nature Physics 19, 670 (2023)](https://www.nature.com/articles/s41567-023-01945-4)
- [Sarkar, Orthey, Augusiak, Nature Physics (2026)](https://doi.org/10.1038/s41567-026-03181-y)
- [Sarkar, arXiv:2502.06986](https://arxiv.org/html/2502.06986)
- [Tavakoli, Abbott, Renou, Gisin, Brunner, arXiv:1805.00377](https://ar5iv.labs.arxiv.org/html/1805.00377)
- [Zhao, Yuan, Ma, arXiv:1607.08002](https://ar5iv.arxiv.org/html/1607.08002)
