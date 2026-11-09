
const chatWindow = document.getElementById("chatWindow");
const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendButton");

function addUserMessage(message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "user-message";

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    messageDiv.appendChild(paragraph);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addBotMessage(message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "bot-message";

    const avatar = document.createElement("div");
    avatar.className = "bot-avatar";
    avatar.textContent = "P";

    const content = document.createElement("div");
    content.className = "message-content";

    const title = document.createElement("strong");
    title.textContent = "PeopleDesk AI";

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    content.appendChild(title);
    content.appendChild(paragraph);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    addUserMessage(message);
    chatInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "...";

    const loadingMessage = document.createElement("p");
    loadingMessage.textContent = "PeopleDesk AI is thinking...";
    loadingMessage.className = "loading-message";
    chatWindow.appendChild(loadingMessage);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        loadingMessage.remove();
        addBotMessage(data.reply || "Sorry, I could not process that.");

    } catch (error) {
        loadingMessage.remove();
        addBotMessage("Unable to connect to the server. Please try again.");
        console.error(error);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "➤";
        chatInput.focus();
    }
}

function sendSuggestion(message) {
    chatInput.value = message;
    sendMessage();
}


// Leave application
const leaveForm = document.getElementById("leaveForm");

leaveForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const reason = document.getElementById("reason").value;

    const message = document.getElementById("leaveMessage");

    if (endDate < startDate) {
        message.textContent = "End date cannot be before start date.";
        return;
    }

    try {
        const response = await fetch("/api/leave", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                start_date: startDate,
                end_date: endDate,
                reason: reason
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.message || "Unable to submit request.";
            return;
        }

        message.textContent = data.message + " Request ID: #" + data.request_id;

        const table = document.getElementById("requestTable");

        const emptyState = table.querySelector(".empty-state");
        if (emptyState) {
            emptyState.parentElement.remove();
        }

        const row = document.createElement("tr");

        [
            "#" + data.request_id,
            startDate,
            endDate,
            reason || "Not specified"
        ].forEach(function(value) {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const statusCell = document.createElement("td");
        const status = document.createElement("span");
        status.className = "status pending";
        status.textContent = "Pending";

        statusCell.appendChild(status);
        row.appendChild(statusCell);

        table.prepend(row);

        leaveForm.reset();

    } catch (error) {
        message.textContent = "Unable to connect to the server.";
        console.error(error);
    }
});