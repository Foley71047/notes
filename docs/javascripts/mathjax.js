// MathJax 配置：$...$ 行内公式，$$...$$ 独立公式，\begin{equation} 自动编号
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
    tags: "ams",
    macros: {
      ket: ["\\left|#1\\right\\rangle", 1],
      bra: ["\\left\\langle#1\\right|", 1],
      braket: ["\\left\\langle#1\\middle|#2\\right\\rangle", 2],
      Tr: "\\operatorname{Tr}",
    },
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

// 与"即时跳转"配合：每次切换页面后重新排版并重置公式编号
document$.subscribe(() => {
  // 首次加载时 MathJax 可能还没就绪，它会在就绪后自行排版
  if (!MathJax.startup || !MathJax.startup.output) return;
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});

// 悬停预览（链接到概念词条时弹出的卡片）是动态插入的，出现后单独排版其中的公式
new MutationObserver((mutations) => {
  if (!window.MathJax || !MathJax.typesetPromise) return;
  for (const m of mutations) {
    for (const node of m.addedNodes) {
      if (node.nodeType === 1 && node.querySelector(".arithmatex")) {
        MathJax.typesetPromise([node]);
      }
    }
  }
}).observe(document.body, { childList: true });
