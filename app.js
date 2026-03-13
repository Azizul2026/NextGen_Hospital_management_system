document.getElementById("loginBtn").addEventListener("click", async function () {

    const role = document.getElementById("role").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            // Save token
            localStorage.setItem("token", data.token);
            localStorage.setItem("role", data.role);

            alert("Login successful!");

            // Redirect based on role
            if (data.role === "admin") {
                window.location.href = "admin_dashboard.html";
            }
            else if (data.role === "doctor") {
                window.location.href = "doctor_dashboard.html";
            }
            else if (data.role === "patient") {
                window.location.href = "patient_dashboard.html";
            }
            else if (data.role === "receptionist") {
                window.location.href = "reception_dashboard.html";
            }

        } else {
            alert(data.message);
        }

    } catch (error) {
        console.error(error);
        alert("Server error. Make sure Flask backend is running.");
    }

});
