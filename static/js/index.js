const textarea = document.querySelector("#code_area");
const runBtn = document.querySelector("#run_btn");
const restore_level = document.querySelector("#restore_level");
const next_list = document.querySelector("#next_list");
const next_level = document.querySelector("#next_level");
const visual_area = document.querySelector(".visual_area");
const code_area = document.querySelector('#code_area')
const original_level_html = visual_area.innerHTML;
const reset_code = document.querySelector("#reset_code");
const previous_level = document.querySelector("#previous_level");


document.addEventListener("DOMContentLoaded", (event) => {
  const user_code = localStorage.getItem('user_code');
  console.log(user_code)
  code_area.value = user_code ? user_code : 'def sort(list):\n    return list' 

});

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


const level = JSON.parse(
  document.getElementById("level-data").textContent
);

function heightFor(value) {
  return Math.trunc(-246.36 + 219.03 * (Math.log(value + 3) / Math.log(3)));
}

async function show_result(result, expected_result) {
  visual_area.innerHTML = "";

  let failed = false;
  for (let i = 0; i < expected_result.length; i++) {
    await new Promise((r) => setTimeout(r, 150));

    const value = result[i];
    let ok;
    if (failed) {
      ok = false;
    } else if (value === expected_result[i]) {
      ok = true;
    } else {
      ok = false;
      failed = true;
    }

    const col = document.createElement("div");
    col.className = "test_column";
    col.style.height = heightFor(value ?? 0) + "px";
    col.style.background = ok
      ? "rgba(203, 255, 59, 0.73)"
      : "rgba(255, 98, 59, 0.73)";
    col.innerHTML = "<p>" + (value ?? "None") + "</p>";
    visual_area.appendChild(col);
  }
}

restore_level.addEventListener("click", () => {
  visual_area.innerHTML = original_level_html;
});

next_list.addEventListener("click", () => {
  localStorage.setItem('user_code', code_area.value)
  window.location.reload();
});

reset_code.addEventListener("click", () => {
  localStorage.removeItem('user_code');
  code_area.value = 'def sort(list):\n    return list'
});

async function show_error(error) {
  visual_area.innerHTML = `
  <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
    <h1 style="font-size: 300%; color: red; margin: 0;">ERROR</h1>
    <h2 style="font-size: 200%; color: red; margin-top: 10px;">${error}</h2>
  </div>
`
}

runBtn.addEventListener("click", async () => {
  const res = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      code: textarea.value,
      level: level,
    }),
  });
  const data = await res.json();
  if (data.ok) {
    console.log(data);
    await show_result(data.result, data.expected_result);
  }else{
    await show_error(data.error)
  }
});

next_level.addEventListener('click', async () =>{
  localStorage.setItem("user_code", code_area.value);
  const current = Number(level.level_number || new URLSearchParams(location.search).get("level") || 1);
  const next = current + 1;

  if (next > 3 || next < 1){
    window.location.href = "/?level=" + 1;
  }else{
    window.location.href = "/?level=" + next;
  }
})

previous_level.addEventListener('click', async () =>{
  localStorage.setItem("user_code", code_area.value);
  const current = Number(level.level_number || new URLSearchParams(location.search).get("level") || 1);
  const prev = current - 1;

  if (prev > 3 || prev < 1){
    window.location.href = "/?level=" + 1;
  }else{
    window.location.href = "/?level=" + prev;
  }
})