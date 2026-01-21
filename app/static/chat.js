let chatReady = false;

/* =========================
   INIT CHAT (PAGE LOAD)
   ❌ DO NOT CREATE SESSION
========================= */
async function initChat() {
    try {
        const res = await fetch("/chatbot/chat/history", {
            method: "GET",
            credentials: "include"
        });

        const historyData = await res.json();

        const chats = Array.isArray(historyData)
            ? historyData
            : historyData.data || [];

        chats.sort(
            (a, b) => new Date(a.created_time) - new Date(b.created_time)
        );

        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = "";

        if (chats.length === 0) {
            chatBox.innerHTML = `
                <div class="message ai">No previous chat history found.</div>
            `;
            chatReady = false; // session not yet created
            return;
        }

        chats.forEach(chat => {
            renderMessage(chat);
        });

        chatBox.scrollTop = chatBox.scrollHeight;
        chatReady = true;

    } catch (error) {
        console.error("Init chat failed:", error);
    }
}

/* =========================
   RENDER MESSAGE (SINGLE SOURCE)
========================= */
function renderMessage(chat) {
    const chatBox = document.getElementById("chat-box");
    const isUser = chat.sender_id !== "medical_ai";
    const senderClass = isUser ? "user" : "ai";
    const senderLabel = isUser ? "You" : "AI";

    chatBox.innerHTML += `
        <div class="message ${senderClass}">
            ${senderLabel}: ${chat.message}
        </div>
    `;
}

/* =========================
   SEND MESSAGE
   ✅ CREATE SESSION ONLY HERE
========================= */
async function sendMessage() {
    const input = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");

    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Create session ONLY if not ready
    if (!chatReady) {
        await fetch("/chatbot/chat", {
            method: "POST",
            credentials: "include"
        });
        chatReady = true;
        chatBox.innerHTML = "";
    }

    // Show user message
    renderMessage({
        sender_id: "user",
        message: userMessage
    });

    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";

    try {
        // Typing indicator
        const typingDiv = document.createElement("div");
        typingDiv.className = "message ai";
        typingDiv.id = "typing";
        typingDiv.innerText = "AI is typing...";
        chatBox.appendChild(typingDiv);

        const response = await fetch("/chatbot/chat/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        document.getElementById("typing")?.remove();

        renderMessage({
            sender_id: "medical_ai",
            message: data.response || data.message
        });

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        document.getElementById("typing")?.remove();
        chatBox.innerHTML += `
            <div class="message ai">Server error</div>
        `;
    }
}

/* =========================
   START NEW CHAT
   ✅ ONLY PLACE SESSION IS RESET
========================= */
async function startNewChat() {
    try {
        await fetch("/chatbot/chat/new", {
            method: "POST",
            credentials: "include"
        });

        document.getElementById("chat-box").innerHTML = "";
        chatReady = true;

    } catch (error) {
        console.error("New chat failed:", error);
    }
}

/* =========================
   MANUAL LOAD HISTORY
========================= */
async function loadChatHistory() {
    try {
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = "";

        const res = await fetch("/chatbot/chat/history", {
            method: "GET",
            credentials: "include"
        });

        const historyData = await res.json();

        // 🔍 DEBUG (always do this first)
        console.log("RAW historyData:", historyData);

        let chats = [];

        // ✅ CORRECT EXTRACTION BASED ON REAL RESPONSE
        if (Array.isArray(historyData)) {
            chats = historyData;
        } else if (Array.isArray(historyData.messages)) {
            chats = historyData.messages;
        }

        console.log("EXTRACTED chats:", chats);
        console.log("Chats length:", chats.length);

        chats.sort(
            (a, b) => new Date(a.created_time) - new Date(b.created_time)
        );

        if (chats.length === 0) {
            chatBox.innerHTML = `
                <div class="message ai">No previous chat history found.</div>
            `;
            chatReady = false;
            return;
        }

        chats.forEach(chat => renderMessage(chat));
        chatBox.scrollTop = chatBox.scrollHeight;
        chatReady = true;

    } catch (error) {
        console.error("History load failed:", error);
    }
}

/* =========================
   SOAP REPORT
========================= */
async function generateSOAPReport() {
    try {
        const res = await fetch("/chatbot/chat/soap", {
            method: "GET",
            credentials: "include"
        });

        const data = await res.json();
        alert("SOAP Report:\n\n" + data.report);

    } catch {
        alert("Failed to generate SOAP report.");
    }
}

/* =========================
   INIT ON PAGE LOAD
========================= */
window.onload = initChat;
