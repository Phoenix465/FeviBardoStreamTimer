const socket = io();
socket.on('connect', function () {
    console.log("Connected");
});

const subscriptionTypeHolderEl = document.getElementById("subscription-type-holder");
const subscriptionTypeEl = document.getElementById("subscription-type");
const subscriptionQuantityLabelEl = document.getElementById("subscription-quantity-label")
const subscriptionQuantityEl = document.getElementById("subscription-quantity")
const applyMessageEl = document.getElementById("apply-message");
const historyEl = document.getElementById("history-table");
const historyRowTemplateEl = document.getElementById("history-row-template");

let settingsChanged = false;

function addSeconds(seconds) {
    socket.emit("addSeconds", {seconds: seconds});
}

document.getElementById('pause').addEventListener('click', function() {
    socket.emit("addSeconds", {seconds: -111.111});
});

function UpdateApplyButtonStatus() {
    const applyButtonEl = document.getElementById("add-subscription");
    if (settingsChanged) {
        applyButtonEl.classList.add("save-active");
        applyButtonEl.classList.remove("save-inactive");
    }
    else {
        applyButtonEl.classList.add("save-inactive");
        applyButtonEl.classList.remove("save-active");
    }
}

function ApplyButtonPressed() {
    if (settingsChanged) {
        // socket.emit("addToTimer", {type: subscriptionTypeEl.textContent, quantity: document.getElementById("subscription-quantity").value});
        socket.emit("addTimerInfo", {
            type: subscriptionTypeEl.getAttribute("data-type"),
            quantity: subscriptionQuantityEl.value
        });
        subscriptionQuantityEl.value = "";
    }

    settingsChanged = false;
    UpdateApplyButtonStatus();
}


document.getElementById("subscription-quantity").addEventListener("input", () => {
    settingsChanged = true;
    UpdateApplyButtonStatus();
});

socket.on('result', function (data) {
    const timeElapsed = Date.now();
    const today = new Date(timeElapsed);

    if (data["type"] === "add-error") {
        applyMessageEl.textContent = `[FAILED] Last Applied at ${today.toUTCString()} due to "${data['reason']}"`
    }
    else if (data["type"] === "add-info") {
        applyMessageEl.textContent = `[SUCCESSFUL] Last Applied at ${today.toUTCString()}"`
    }
    else if (data["type"] === "history-update") {
        historyEl.innerHTML = "";
        for (const info of data["history"]) {
            let rowEl = historyRowTemplateEl.innerHTML;
            rowEl = rowEl.replaceAll("..1", info["#"])
            rowEl = rowEl.replaceAll("..2", info["type"])
            rowEl = rowEl.replaceAll("..3", info["quantity"])
            rowEl = rowEl.replaceAll("..4", Math.round(info["seconds"] * 100) / 100)
            rowEl = rowEl.replaceAll("..5", Math.round(info["points"] * 100) / 100)

            historyEl.insertAdjacentHTML("beforeend", rowEl);
        }
    }
    else if (data["type"] === "update-pause") {
        if (data["paused"]) {
            document.getElementById("pause").textContent = "Unpause";
        }
        else {
            document.getElementById("pause").textContent = "Pause";
        }
    }
});


for (const child of subscriptionTypeHolderEl.children) {
    child.addEventListener("click", function () {
        subscriptionTypeEl.textContent = child.textContent;
        subscriptionTypeEl.setAttribute("data-unit", child.getAttribute("data-unit"));
        subscriptionTypeEl.setAttribute("data-type", child.getAttribute("data-type"));

        subscriptionQuantityLabelEl.textContent = "QUANTITY"
        const unit = child.getAttribute("data-unit")
        if (unit !== "") {
            subscriptionQuantityLabelEl.textContent += ` [${unit}]`

            settingsChanged = true;
            UpdateApplyButtonStatus();
        }
    });
}

function ForceUpdateHistory() {
    socket.emit("getHistory");
}

setInterval(ForceUpdateHistory, 2000);
socket.emit("getHistory");
