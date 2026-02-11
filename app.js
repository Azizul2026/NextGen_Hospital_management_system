document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginBtn").addEventListener("click", login);
});

function login() {
    const role = document.getElementById("role").value;
    const user = document.getElementById("username").value.trim();
    const pass = document.getElementById("password").value.trim();

    if (role === "admin" && user === "admin" && pass === "admin") {
        window.location.href = "dashboard.html";
    }
    else if (role === "doctor" && user === "doctor" && pass === "doctor") {
        window.location.href = "doctor.html";
    }
    else if (role === "patient" && user === "patient" && pass === "patient") {
        window.location.href = "patient.html";
    }
    else {
        alert("Invalid Credentials");
    }
}
