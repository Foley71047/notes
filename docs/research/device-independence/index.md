---
title: 器件无关与网络非局域性
description: 器件无关（DI）认证、Bell 非局域性与网络场景的学习与研究笔记。
icon: lucide/orbit
hide:
  - tags
---

# 器件无关与网络非局域性

器件无关（device-independent, DI）的核心问题是：**如果完全不信任实验设备，只看输入—输出的概率表，还能对设备内部得出什么结论？** 这个主题收集我在这方面的学习梳理，以及它们和我自己项目（用星型网络认证纠缠测量的纠缠深度）的对应关系。

## 文章

<div class="grid cards" markdown>

-   :lucide-box:{ .lg .middle } __器件无关（DI）到底在讲什么__

    ---

    从"假设记账"出发：黑盒与概率表、DI 的最小假设集、验证者与对手、七步设计配方、self-testing 的等价类、半 DI 谱系。

    [:lucide-arrow-right: 阅读](di-primer.md)

-   :lucide-radio-tower:{ .lg .middle } __无信号原理与源的假设__

    ---

    无信号原理约束的是关联 $P$，源的假设约束的是因果结构——前者推不出后者。$\mathcal L\subset\mathcal Q\subset\mathcal{NS}$、三种"独立"、源假设阶梯与凸性判据。

    [:lucide-arrow-right: 阅读](no-signalling-and-sources.md)

</div>

## 建议阅读顺序

1. 先读 [器件无关（DI）到底在讲什么](di-primer.md)，建立"只看概率表"的视角和假设清单；
2. 再读 [无信号原理与源的假设](no-signalling-and-sources.md)，弄清网络场景里多出来的那条独立性假设。
