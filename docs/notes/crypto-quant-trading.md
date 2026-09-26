---
description: 一本面向零基础的系统教材（PDF，117 页）：交易机制、风险管理、市场数据、策略范式、技术分析批判、量化路径与风险清单。
type: 量化分析
tags:
  - 量化
---

# 加密货币交易：从零到量化

这是我让 claude code 给我写的面向零基础学习者的初步加密货币交易教材，在我修改几次过后，内容依旧难免有差错，一些计算主要是在估算水平，比如计算连续收益时没算持仓价值变化等等不严谨之处，但是这本书总体的机制介绍还是值得一看，如果你和我一样也刚进市场。
{ .page-lead }

!!! warning "阅读前请注意"
    本书**不构成任何投资建议**。书中所有交易所参数（手续费、杠杆上限、维持保证金率、资金费率等）都是写作时（2026 年 8 月）的大致情况，交易所随时会调整，**一切以 OKX 官方文档为准**；书中用【待核实】标出的地方，下单前必须自己核实。

<div class="fl-pdf" markdown>
<div class="fl-pdf__bar" markdown>
<p class="fl-pdf__name" markdown="span">:lucide-file-text: 加密货币交易：从零到量化 <small>PDF · 117 页 · 1.8 MB</small></p>
<p class="fl-pdf__actions" markdown>[:lucide-external-link: 新标签打开](crypto-quant-trading.pdf){ .md-button target="_blank" rel="noopener" } [:lucide-download: 下载 PDF](crypto-quant-trading.pdf){ .md-button .md-button--primary download }</p>
</div>
<iframe class="fl-pdf__frame" src="crypto-quant-trading.pdf#view=FitH" title="加密货币交易：从零到量化" loading="lazy"></iframe>
<p class="fl-pdf__mobile">手机浏览器对内嵌 PDF 的支持有限，建议点击上方按钮下载，或在新标签页中打开阅读。</p>
</div>

## 这本书的写法
这本书大致讲法分为机制介绍、实例介绍、还有相关内容加密市场的一些重大事件，这种编排方式让我理解机制更深刻、对市场的认知更加具体




## 目录

??? abstract "第一部分　交易机制基础"
    订单簿与撮合（价格优先、时间优先）· 限价单与市价单、Maker 与 Taker · OKX 订单类型 · 手续费、滑点与冲击成本 · 现货、杠杆、交割合约与永续合约 · 合约面值 · 标记价格与指数价格 · 永续合约与资金费率 · 保证金、维持保证金与强制平仓 · U 本位与币本位合约的强平价推导 · 逐仓与全仓 · 穿仓、风险准备金与自动减仓（ADL）· 一次完整交易的成本清单

??? abstract "第二部分　风险管理与仓位"
    亏损的不对称性 · 单笔风险预算 · 连续亏损是必然的 · 最大回撤与破产概率 · Kelly 公式与分数 Kelly · 波动率目标法与 ATR 仓位 · 心理与执行纪律

??? abstract "第三部分　市场结构与数据"
    未平仓合约（Open Interest）· 资金费率历史 · 清算数据 · 多空比 · 链上数据及其可信度 · 抵押品由谁定价 · USDT/USDC 与稳定币风险 · 在 OKX 上获取数据 · 被自媒体系统性误读的数据

??? abstract "第四部分　策略范式"
    趋势跟踪 · 均值回复 · 期现套利（Cash-and-Carry）· 资金费率套利 · 跨交易所套利 · 事件驱动与机制性崩溃（LUNA/UST、Mango Markets 预言机操纵）· 策略的拥挤度与容量

??? abstract "第五部分　技术分析：批判性的一章"
    有机制解释的部分（挂单堆积、止损簇与流动性猎取、自我实现的协调点）· 证据薄弱的部分（形态学的不可证伪、斐波那契、艾略特波浪、江恩）· 一个必须理解的统计陷阱 · 术语词典

??? abstract "第六部分　通往量化的路径"
    写第一行代码之前 · 数据管道 · 回测框架的基本设计 · 回测陷阱（前视偏差、幸存者偏差、多重检验、过拟合）· 样本外验证与 Walk-Forward · 评估指标 · OKX API 使用要点与常见坑

??? abstract "第七部分　风险清单"
    交易所风险（你的余额不是你的钱）· 合约特有风险 · 技术与 API 风险 · 私钥与账户安全 · 骗局模式识别 · 中国大陆用户的特殊风险 · 总检查清单

??? abstract "附录"
    A. 待核实清单 · B. 核实状态说明（含第一版犯过的错）· C. 延伸阅读 · D. 一份 90 天的学习计划
