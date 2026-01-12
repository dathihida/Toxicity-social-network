
(function injectCSS() {
  const style = document.createElement("style");
  style.textContent = `
    .toxic-blur {
      filter: blur(6px);
      user-select: none;
      cursor: pointer;
    }
    .toxic-label {
      margin-top: 4px;
      font-size: 12px;
      color: red;
      font-weight: 600;
    }
  `;
  document.head.appendChild(style);
})();

//Cache 
const checkedText = new Set();

// Call API
async function checkToxicity(text) {
  try {
    const res = await fetch("http://localhost:8000/api/v1/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();
    return data.toxic === true;
  } catch (err) {
    console.error("[FB Toxic API error]", err);
    return false;
  }
}


async function processComment(el) {
  const text = el.innerText.trim();
  if (!text || checkedText.has(text)) return;


  if (text.length < 5) return;


  if (!el.closest('[role="article"]')) return;

  checkedText.add(text);

  const isToxic = await checkToxicity(text);
  if (!isToxic) return;

  el.classList.add("toxic-blur");

  if (!el.nextSibling || !el.nextSibling.classList?.contains("toxic-label")) {
    const label = document.createElement("div");
    label.className = "toxic-label";
    label.innerText = "Bình luận tiêu cực (bấm để xem)";
    el.after(label);

    el.addEventListener("click", () => {
      el.classList.toggle("toxic-blur");
    });
  }
}

// ===== Scan page =====
function scanFacebookComments() {
  document
    .querySelectorAll('span[dir="auto"][lang]')
    .forEach(processComment);
}

// ===== Observe DOM =====
const observer = new MutationObserver(() => {
  scanFacebookComments();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

console.log("[FB Toxic Filter] loaded");
