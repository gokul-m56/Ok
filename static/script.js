
// Create Account
function createUser() {
    fetch("/create_user", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("name").value,
            phone: document.getElementById("phone").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("msg").innerText =
            "Account Created! USER ID: " + data.user_id;
    });
}


// Verify User
function verifyUser() {
    fetch("/verify_user", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: document.getElementById("v_user").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("msg").innerText = data.message;
    });
}


// Recharge
function recharge() {
    fetch("/recharge", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: document.getElementById("r_user").value,
            amount: document.getElementById("amount").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("msg").innerText =
            data.message + " | New Balance: ₹" + data.balance;
    });
}


// Check Balance
function getBalance() {
    fetch("/get_balance", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: document.getElementById("b_user").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("balance").innerText =
            "Current Balance: ₹" + data.balance;
    });
}
