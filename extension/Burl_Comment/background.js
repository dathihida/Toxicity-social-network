chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CLASSIFY") {
    fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        comment: message.comment,
        title: message.title,
        topic: message.topic
      })
    })
      .then(res => res.json())
      .then(data => sendResponse(data))
      .catch(err => {
        console.error("API error:", err);
        sendResponse({ error: true });
      });

    return true; // async
  }
});
