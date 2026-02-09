function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    if (user === "admin" && pass === "admin") {
        window.location.href = "dashboard.html";
    } else {
        alert("Invalid Credentials");
    }
}

function logout() {
    window.location.href = "index.html";
}
