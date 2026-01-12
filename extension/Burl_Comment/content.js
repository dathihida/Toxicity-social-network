// require('dotenv').config();

const TOXIC_CLASS = "toxic-blur";
const API_KEY = API_KEY_YOU;

(function injectCSS() {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = chrome.runtime.getURL("styles.css");
  document.head.appendChild(link);
})();

// VIDEO ID 
function getVideoId() {
  const url = new URL(location.href);

  //?v=VIDEO_ID
  const v = url.searchParams.get("v");
  if (v) return v;

  ///shorts/VIDEO_ID
  const shortsMatch = url.pathname.match(/\/shorts\/([^/?]+)/);
  if (shortsMatch) return shortsMatch[1];

  const shortLinkMatch = url.hostname === "youtu.be"
    ? url.pathname.replace("/", "")
    : null;

  if (shortLinkMatch) return shortLinkMatch;

  return null;
}


// CATEGORY MAP 
const CATEGORY_MAP_V = {
  "1": "PhimAnh",
  "2": "OtoXeMay",
  "10": "Giaitri",
  "15": "DongVat",
  "17": "TheThao",
  "20": "Gaming",
  "21": "CuocSong",
  "22": "TheGioi",
  "23": "GiaiTri",
  "24": "GiaiTri",
  "25": "ThoiSu",
  "26": "PhongCach",
  "27": "GiaoDuc",
  "28": "KhoaHoc",
};

const CATEGORY_MAP_E = {
  "1": "Film & Animation",
  "2": "Autos & Vehicles",
  "10": "Music",
  "15": "Pets & Animals",
  "17": "Sports",
  "18": "Short Movies",
  "20": "Gaming",
  "21": "Videoblogging",
  "22": "People & Blogs",
  "23": "Comedy",
  "24": "Entertainment",
  "25": "News & Politics",
  "26": "Howto & Style",
  "27": "Education",
  "28": "Science & Technology",
  "29": "Nonprofits & Activism",
  "30": "Movies",
  "31": "Anime/Animation",
  "32": "Action/Adventure",
  "33": "Classics",
  "34": "Comedy",
  "35": "Documentary",
  "36": "Drama",
  "37": "Family",
  "38": "Foreign",
  "39": "Horror",
  "40": "Sci-Fi/Fantasy",
  "41": "Thriller",
  "42": "Shorts",
  "43": "Shows",
  "44": "Trailers"
};

// FETCH VIDEO META
let VIDEO_META = null;

async function fetchVideoMeta() {
  if (VIDEO_META) return VIDEO_META;

  const videoId = getVideoId();
  if (!videoId) return null;

  const url =
    `https://www.googleapis.com/youtube/v3/videos` +
    `?part=snippet&id=${videoId}&key=${API_KEY}`;

  const res = await fetch(url);
  const data = await res.json();

  if (!data.items || !data.items.length) return null;

  const snippet = data.items[0].snippet;

  VIDEO_META = {
    title: snippet.title,
    topic: CATEGORY_MAP_E[snippet.categoryId] || "Unknown"
  };

  return VIDEO_META;
}

//  BLUR 
function applyBlur(el, confidence, source) {
  el.classList.add(TOXIC_CLASS);

  const overlay = document.createElement("div");
  overlay.className = "toxic-overlay";
  overlay.textContent =
    `Bình luận bị ẩn (Toxic ${(confidence).toFixed(1)}%) - (${source}) – Nhấn để xem`;

  overlay.onclick = () => {
    el.classList.remove(TOXIC_CLASS);
    overlay.remove();
  };

  el.after(overlay);
}

// CLASSIFY COMMENT
async function classifyComment(text, el) {
  const meta = await fetchVideoMeta();
  if (!meta) return;

  chrome.runtime.sendMessage(
    {
      type: "CLASSIFY",
      comment: text,
      title: meta.title,
      topic: meta.topic
    },
    (res) => {
      if (!res || res.error) return;
      if (res.toxic) {
        applyBlur(el, res.confidence || 0, res.source);
      }
    }
  );
}

// NORMAL COMMENT 
const scannedComments = new WeakSet();

function processComment(el) {
  if (scannedComments.has(el)) return;
  scannedComments.add(el);

  const text = el.textContent.trim();
  if (text.length < 5) return;

  classifyComment(text, el);
}

function scanComments() {
  document
    .querySelectorAll("#content-text")
    .forEach(processComment);
}

// COMMENT OBSERVER
const commentObserver = new MutationObserver(scanComments);

commentObserver.observe(document.body, {
  childList: true,
  subtree: true
});

scanComments();

// LIVE CHAT
if (location.href.includes("live_chat")) {
  console.log("Live chat detected");

  const scannedLive = new WeakSet();

  function handleLiveMessage(el) {
    if (scannedLive.has(el)) return;
    scannedLive.add(el);

    const text = el.innerText?.trim();
    if (!text || text.length < 3) return;

    classifyComment(text, el);
  }

  function observeLiveChat() {
    const chat = document.querySelector(
      "yt-live-chat-item-list-renderer #items"
    );

    if (!chat) {
      setTimeout(observeLiveChat, 500);
      return;
    }

    const liveChatObserver = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (!(node instanceof HTMLElement)) continue;

          const msg = node.querySelector?.(
            "yt-live-chat-text-message-renderer #message"
          );
          if (msg) handleLiveMessage(msg);
        }
      }
    });

    liveChatObserver.observe(chat, { childList: true });
    console.log(" Live chat observer attached");
  }

  document
    .querySelectorAll("yt-live-chat-text-message-renderer #message")
    .forEach(handleLiveMessage);

  observeLiveChat();
}
