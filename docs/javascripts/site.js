// 笔记入口页的类型筛选、标签页的单标签视图。
// 列表本身由 scripts/site_data.py 在构建时生成；没有 JavaScript 时显示全部内容。

function flNotesFilter(root) {
  const buttons = root.querySelectorAll(".fl-filter__btn");
  const notes = root.querySelectorAll(".fl-note");
  const empty = root.querySelector(".fl-notes__empty");

  const apply = (type) => {
    let shown = 0;
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.type === type)));
    notes.forEach((n) => {
      n.hidden = type !== "" && n.dataset.type !== type;
      if (!n.hidden) shown += 1;
    });
    if (empty) empty.hidden = shown > 0;
    // 把当前筛选写进网址（?type=研究），刷新或分享链接时保持
    const url = new URL(location.href);
    if (type) url.searchParams.set("type", type);
    else url.searchParams.delete("type");
    history.replaceState(history.state, "", url);
  };

  buttons.forEach((b) => b.addEventListener("click", () => apply(b.dataset.type)));
  const initial = new URLSearchParams(location.search).get("type") || "";
  apply([...buttons].some((b) => b.dataset.type === initial) ? initial : "");
}

function flTagsView(root) {
  root.dataset.js = "";
  const update = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = id && document.getElementById(id);
    const active = target && target.classList.contains("fl-tag-section") ? target : null;
    root.classList.toggle("fl-tags--single", Boolean(active));
    root.querySelectorAll(".fl-tag-section").forEach((s) => s.classList.toggle("is-active", s === active));
    root.querySelectorAll(".fl-tag-chip").forEach((c) =>
      c.classList.toggle("is-active", Boolean(active) && c.getAttribute("href") === "#" + active.id));
  };
  update();
  window.addEventListener("hashchange", update);
  // 即时导航可能不触发 hashchange，点击后再同步一次
  root.addEventListener("click", (e) => {
    if (e.target.closest("a")) setTimeout(update, 0);
  });
}

document$.subscribe(() => {
  document.querySelectorAll("[data-fl-notes]").forEach(flNotesFilter);
  document.querySelectorAll("[data-fl-tags]").forEach(flTagsView);
});
