const textarea = document.querySelector("#code_area");


textarea.addEventListener("keydown", (e) => {
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  if (e.key === "Tab") {
    e.preventDefault();
    textarea.setRangeText("    ", start, end, "end");
    return;
  }
  if (e.key === "(") {
    e.preventDefault();
    const selected = textarea.value.slice(start, end);
    textarea.setRangeText(`(${selected})`, start, end, "end");
    if (!selected) textarea.selectionStart = textarea.selectionEnd = start + 1;
  }
});