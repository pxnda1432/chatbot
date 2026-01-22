// ✅ This alert proves script.js is LOADED
alert("✅ script.js loaded successfully");

function send() {
  // ✅ This alert proves button click works
  alert("✅ Send button clicked");

  let inputBox = document.getElementById("msg");
  let chatbox = document.getElementById("chatbox");

  let msg = inputBox.value.trim();

  // ✅ This alert proves message is captured
  alert("📨 Message typed: " + msg);

  if (msg === "") {
    alert("⚠️ Empty message");
    return;
  }

  // Show user message
  chatbox.innerHTML += "<b>You:</b> " + msg + "<br>";

  // Send to backend
  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: msg })
  })
  .then(response => {
    alert("✅ Backend responded");
    return response.json();
  })
  .then(data => {
    alert("🤖 Bot reply received: " + data.reply);
    chatbox.innerHTML += "<b>Bot:</b> " + data.reply + "<br>";
  })
  .catch(error => {
    alert("❌ Fetch error");
    chatbox.innerHTML += "<b>Bot:</b> Server error<br>";
  });

  // Clear input
  inputBox.value = "";
}
