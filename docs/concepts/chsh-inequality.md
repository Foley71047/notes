---
en: CHSH inequality
statement: '局域隐变量模型下 $\lvert\langle A_0B_0\rangle+\langle A_0B_1\rangle+\langle A_1B_0\rangle-\langle A_1B_1\rangle\rvert\le 2$'
description: 局域隐变量模型下，CHSH 组合 S 的绝对值不超过 2。
tags:
  - Bell 非局域性
  - 器件无关
---

# CHSH 不等式

!!! theorem "陈述"
    两方 Alice、Bob 各自从两个测量 $x,y\in\{0,1\}$ 中选一个，得到结果 $a,b\in\{+1,-1\}$。记关联函数
    $E_{xy}=\sum_{a,b}ab\,p(ab|xy)$。若关联存在局域隐变量模型

    $$p(ab|xy)=\int d\lambda\,q(\lambda)\,p(a|x,\lambda)\,p(b|y,\lambda),$$

    则

    $$S=E_{00}+E_{01}+E_{10}-E_{11},\qquad \lvert S\rvert\le 2 .$$

## 直观含义

如果测量结果在测量之前就由某个共同原因 $\lambda$ 决定、而且每一方的结果只依赖自己的设置，那么四个关联不可能"同时都很强"：前三项都取 $+1$ 时，第四项被迫也取 $+1$，于是 $S$ 最多是 2。实验测到 $\lvert S\rvert>2$，就说明不存在这样的局域解释——这就是 **Bell 非局域性**。

结论只用到概率表 $p(ab|xy)$，不涉及设备内部的物理实现，所以它是器件无关（DI）方案的基本工具。

## 成立条件

- **场景**：两方、每方两个设置、结果取 $\pm1$（多值结果要先映射到 $\pm1$）。
- **局域性**：Alice 的结果只依赖 $x$ 和 $\lambda$，不依赖 Bob 的设置 $y$，反之亦然。
- **测量独立性**：$\lambda$ 的分布 $q(\lambda)$ 与设置 $(x,y)$ 无关（自由选择）。
- **实验上**还要关掉漏洞：空间类隔离（locality loophole）、足够高的探测效率（detection loophole）、独立的随机数源（freedom-of-choice loophole）。

不需要假设量子力学、希尔伯特空间维数或设备的工作原理。

## 证明思路

1. 局域模型是局域确定性策略的凸组合，而 $S$ 对 $p$ 是线性的，所以只需检查确定性策略。
2. 固定 $\lambda$ 时，结果是确定的数 $a_0,a_1,b_0,b_1\in\{\pm1\}$，此时

    $$S_\lambda=a_0(b_0+b_1)+a_1(b_0-b_1).$$

3. $b_0+b_1$ 和 $b_0-b_1$ 中恰好一个是 0、另一个是 $\pm2$，所以 $S_\lambda=\pm2$。
4. 对 $q(\lambda)$ 取平均，$\lvert S\rvert\le\int d\lambda\,q(\lambda)\lvert S_\lambda\rvert=2$。

## 何时取等

$S=2$ 由局域确定性策略取到，例如所有结果都输出 $+1$：$S=1+1+1-1=2$。16 个确定性策略里恰有 8 个取到 $S=2$，它们张成局域多面体的一个面（facet），所以 CHSH 不等式是**紧的** Bell 不等式。

## 相关结果

- [Tsirelson 界](tsirelson-bound.md)：量子力学允许的最大值是 $2\sqrt2$，达到时可以自检验最大纠缠态。
- 无信号（NS）关联最多可以达到 $S=4$（PR box），所以 $2<2\sqrt2<4$ 把局域、量子、无信号三个集合分开。
- Fine 定理：在两方、两设置、两结果的场景里，CHSH 不等式（及其重标记）连同正性条件完全刻画了局域多面体。
- 探测效率：用最大纠缠态检验 CHSH 需要效率高于 $2/(1+\sqrt2)\approx82.8\%$；Eberhard 用非最大纠缠态把门槛降到约 $2/3$。
- 原始文献：J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, *PRL* **23**, 880 (1969)。
