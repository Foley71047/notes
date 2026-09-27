---
en: Concurrence
statement: '两量子比特态的纠缠度量：纯态 $C=\lvert\braket{\psi}{\tilde\psi}\rvert$，混态由 Wootters 公式 $C=\max(0,\lambda_1-\lambda_2-\lambda_3-\lambda_4)$ 给出，$C>0$ 当且仅当态纠缠'
description: 并发度是两量子比特系统上可解析计算的纠缠度量，取值 0 到 1，与形成纠缠一一对应。
tags:
  - 纠缠
  - 资源理论
---

# 并发度（Concurrence）

!!! definition "定义"
    **纯态。** 对两量子比特纯态 $\ket{\psi}$，定义自旋翻转态 $\ket{\tilde\psi}=(\sigma_y\otimes\sigma_y)\ket{\psi^*}$（$^*$ 表示在计算基下取复共轭），并发度为

    $$C(\psi)=\lvert\braket{\psi}{\tilde\psi}\rvert .$$

    若 $\ket{\psi}=a\ket{00}+b\ket{01}+c\ket{10}+d\ket{11}$，则 $C(\psi)=2\lvert ad-bc\rvert$。

    **混态。** 对混态 $\rho$，用凸顶（convex roof）推广：

    $$C(\rho)=\min_{\{p_i,\psi_i\}}\sum_i p_i\,C(\psi_i),$$

    最小值取遍所有满足 $\rho=\sum_i p_i\ket{\psi_i}\bra{\psi_i}$ 的纯态分解。Wootters 证明了它有闭式解：令 $\tilde\rho=(\sigma_y\otimes\sigma_y)\rho^*(\sigma_y\otimes\sigma_y)$，$\lambda_1\ge\lambda_2\ge\lambda_3\ge\lambda_4$ 为 $\rho\tilde\rho$ 的本征值的平方根（等价地，$\sqrt{\sqrt\rho\,\tilde\rho\,\sqrt\rho}$ 的本征值），则

    $$C(\rho)=\max\{0,\ \lambda_1-\lambda_2-\lambda_3-\lambda_4\}.$$

    $0\le C\le 1$，$C=0$ 当且仅当 $\rho$ 可分，$C=1$ 对应最大纠缠态。

## 直观含义

$\sigma_y$ 加复共轭这个操作叫"自旋翻转"，它把单个量子比特的任意纯态映成与之正交的态（Bloch 矢量反向）。因此：

- 对积态 $\ket{a}\ket{b}$，两个比特各自被翻到正交态，$\braket{\psi}{\tilde\psi}=0$，并发度为零；
- 对 Bell 态，自旋翻转只改变一个整体相位，重叠为 $1$，并发度最大。

所以并发度衡量的是"这个态在自旋翻转下有多像它自己"——越不像积态，越能保持不变。

对纯态，它也可以用约化态写出：

$$C(\psi)=\sqrt{2\left(1-\Tr\rho_A^2\right)}=2\sqrt{\det\rho_A},\qquad \rho_A=\Tr_B\ket{\psi}\bra{\psi},$$

即约化态越混，纠缠越大。

并发度本身是纠缠单调量，但它最重要的地位来自与**形成纠缠**（entanglement of formation）的一一对应：

$$E_F(\rho)=h\!\left(\frac{1+\sqrt{1-C(\rho)^2}}{2}\right),\qquad h(x)=-x\log_2x-(1-x)\log_2(1-x).$$

$E_F$ 是 $C$ 的单调递增函数，而 $E_F$ 原本是一个难算的凸顶优化，借助并发度在两量子比特上就能直接算出。这是并发度被提出的初衷。

## 例子

!!! example "例 1：部分纠缠纯态"
    $\ket{\psi}=\cos\theta\ket{00}+\sin\theta\ket{11}$。这里 $a=\cos\theta,\ d=\sin\theta,\ b=c=0$，所以

    $$C=2\lvert\cos\theta\sin\theta\rvert=\lvert\sin2\theta\rvert .$$

    $\theta=0$ 时是积态，$C=0$；$\theta=\pi/4$ 时是 Bell 态 $\ket{\Phi^+}$，$C=1$。

!!! example "例 2：Werner 态"
    $\rho_p=p\ket{\Psi^-}\bra{\Psi^-}+(1-p)\dfrac{\mathbb 1}{4}$，$0\le p\le1$。

    $\ket{\Psi^-}$ 在自旋翻转下不变，$\rho_p$ 又是实矩阵，所以 $\tilde\rho_p=\rho_p$，$\lambda_i$ 就是 $\rho_p$ 自己的本征值：$\frac{1+3p}{4}$（一重）和 $\frac{1-p}{4}$（三重）。于是

    $$C(\rho_p)=\max\left\{0,\ \frac{1+3p}{4}-3\cdot\frac{1-p}{4}\right\}=\max\left\{0,\ \frac{3p-1}{2}\right\}.$$

    Werner 态在 $p>1/3$ 时纠缠，与 PPT 判据给出的阈值一致。

## 相关结果

- **形成纠缠**：两量子比特上 $E_F$ 是 $C$ 的单调函数（见上文公式）[^wootters]。
- **负性**：对两量子比特态，负性 $N(\rho)=\lVert\rho^{T_B}\rVert_1-1$ 满足 $N\le C$，纯态时取等 [^verstraete]。
- **纠缠一夫一妻制（CKW 不等式）**：三量子比特纯态满足 $C_{AB}^2+C_{AC}^2\le C_{A(BC)}^2$，其中 $C_{A(BC)}=2\sqrt{\det\rho_A}$；差值定义了三体纠缠（tangle）[^ckw]。
- **高维推广**：I-并发度 $C(\psi)=\sqrt{2(1-\Tr\rho_A^2)}$ 对任意维数纯态有定义，但混态的凸顶一般没有 Wootters 式的闭式解 [^rungta]。

[^wootters]: W. K. Wootters, *Entanglement of Formation of an Arbitrary State of Two Qubits*, Phys. Rev. Lett. **80**, 2245 (1998)；纯态和秩 2 情形见 S. Hill and W. K. Wootters, Phys. Rev. Lett. **78**, 5022 (1997)。
[^verstraete]: F. Verstraete, K. Audenaert, J. Dehaene, B. De Moor, *A comparison of the entanglement measures negativity and concurrence*, J. Phys. A **34**, 10327 (2001)。
[^ckw]: V. Coffman, J. Kundu, W. K. Wootters, *Distributed entanglement*, Phys. Rev. A **61**, 052306 (2000)。
[^rungta]: P. Rungta, V. Bužek, C. M. Caves, M. Hillery, G. J. Milburn, *Universal state inversion and concurrence in arbitrary dimensions*, Phys. Rev. A **64**, 042315 (2001)。
