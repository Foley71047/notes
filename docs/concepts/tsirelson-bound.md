---
en: Tsirelson's bound
statement: '量子力学中 CHSH 值满足 $\lvert S\rvert\le 2\sqrt2$'
description: 量子力学中 CHSH 组合 S 的绝对值不超过 2√2，最大纠缠态配合适当测量可以取到。
tags:
  - Bell 非局域性
  - 半定规划
---

# Tsirelson 界

!!! theorem "陈述"
    对任意量子态 $\rho$（任意维数）和任意满足 $-\mathbb 1\le A_x,B_y\le\mathbb 1$ 的观测量，定义 CHSH 算符

    $$\mathcal B=A_0\otimes B_0+A_0\otimes B_1+A_1\otimes B_0-A_1\otimes B_1,$$

    则

    $$\lvert S\rvert=\lvert\Tr(\rho\,\mathcal B)\rvert\le 2\sqrt2 .$$

## 直观含义

量子关联比局域关联强（[CHSH 不等式](chsh-inequality.md)的局域上界是 2），但又没有强到无信号原理允许的极限 4。实验测到 $2<S\le2\sqrt2$ 说明存在非局域性，而测到 $S>2\sqrt2$ 则说明连量子力学也解释不了（或者实验有问题）。

## 成立条件

- **量子理论**：概率由 Born 规则 $p(ab|xy)=\Tr[\rho\,(M_{a|x}\otimes N_{b|y})]$ 给出。
- **两方测量相容**：张量积结构 $A_x\otimes B_y$，或者更一般地 $[A_x,B_y]=0$（对易算子框架）。
- **观测量有界**：本征值在 $[-1,1]$ 内，也就是结果取 $\pm1$ 时的期望值。

态可以是混合态、维数不限，所以这是器件无关的上界。只假设无信号原理是不够的：PR box 满足无信号却能达到 $S=4$。

## 证明思路

先考虑 $A_x^2=B_y^2=\mathbb 1$（投影测量；一般情形用 Naimark 扩张化归到这里）。

=== "平方和（SOS）分解"

    直接展开可以验证

    $$2\sqrt2\,\mathbb 1-\mathcal B=\frac{1}{\sqrt2}\left[\Big(A_0-\tfrac{B_0+B_1}{\sqrt2}\Big)^2+\Big(A_1-\tfrac{B_0-B_1}{\sqrt2}\Big)^2\right]\ge0,$$

    所以 $\mathcal B\le2\sqrt2\,\mathbb 1$。这个分解正是 NPA 层级第一层半定规划（SDP）的对偶证书。

=== "平方技巧"

    计算得 $\mathcal B^2=4\,\mathbb 1-[A_0,A_1]\otimes[B_0,B_1]$。由于 $\lVert[A_0,A_1]\rVert\le2$、$\lVert[B_0,B_1]\rVert\le2$，得 $\lVert\mathcal B\rVert^2\le8$，即 $\lVert\mathcal B\rVert\le2\sqrt2$。

## 何时取等

取最大纠缠态 $\ket{\Phi^+}=\frac{1}{\sqrt2}(\ket{00}+\ket{11})$ 和

$$A_0=Z,\quad A_1=X,\quad B_0=\frac{Z+X}{\sqrt2},\quad B_1=\frac{Z-X}{\sqrt2},$$

四个关联依次是 $\frac{1}{\sqrt2},\frac{1}{\sqrt2},\frac{1}{\sqrt2},-\frac{1}{\sqrt2}$，所以 $S=2\sqrt2$。

反过来，由 SOS 分解，取等要求 $A_0\ket\psi=\frac{B_0+B_1}{\sqrt2}\ket\psi$、$A_1\ket\psi=\frac{B_0-B_1}{\sqrt2}\ket\psi$，由此可推出双方的两个观测量在态的支撑上反对易。于是在局域等距变换下，态只能是 $\ket{\Phi^+}$（外加无关的辅助系统），测量只能是上面那组——这就是 CHSH 的**自检验**（self-testing）。

## 相关结果

- [CHSH 不等式](chsh-inequality.md)：局域隐变量模型的上界 2。
- NPA 层级：用一列半定规划从外部逼近量子关联集合，对 CHSH 第一层就给出精确的 $2\sqrt2$。
- 自检验的稳健版本：$S$ 接近 $2\sqrt2$ 时，态接近 $\ket{\Phi^+}$，保真度随偏差连续变化。
- 原始文献：B. S. Cirel'son, *Lett. Math. Phys.* **4**, 93 (1980)。
