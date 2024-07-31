const socket = io();
socket.on('connect', function () {
    console.log("Connected");
});

const subscriptionTypeHolderEl = document.getElementById("subscription-type-holder");
const subscriptionTypeEl = document.getElementById("subscription-type");
const subscriptionQuantityLabelEl = document.getElementById("subscription-quantity-label")

let settingsChanged = false;

function addSeconds(seconds) {
    socket.emit("addSeconds", {seconds: seconds});
}

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
        socket.emit("addSeconds", {seconds: 10});
    }

    settingsChanged = false;
    UpdateApplyButtonStatus();
}



document.getElementById("subscription-quantity").addEventListener("input", () => {
    settingsChanged = true;
    UpdateApplyButtonStatus();
});


console.log(subscriptionTypeHolderEl)
for (const child of subscriptionTypeHolderEl.children) {
    child.addEventListener("click", function () {
        subscriptionTypeEl.textContent = child.textContent;

        subscriptionQuantityLabelEl.textContent = "QUANTITY"
        const unit = child.getAttribute("data-unit")
        if (unit !== "") {
            subscriptionQuantityLabelEl.textContent += ` [${unit}]`
        }
    });
}