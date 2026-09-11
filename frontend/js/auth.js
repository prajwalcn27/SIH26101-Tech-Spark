/* =========================================
   TECH SPARK - AUTHENTICATION
   SIH26101
========================================= */


/* -----------------------------------------
   SELECT ROLE
----------------------------------------- */

function selectRole(role) {

    // Get all role buttons
    const roleButtons = document.querySelectorAll(".role-option");

    // Remove active state
    roleButtons.forEach(button => {
        button.classList.remove("active");
    });

    // Add active state to selected role
    const selectedButton =
        document.querySelector(`[data-role="${role}"]`);

    if (selectedButton) {
        selectedButton.classList.add("active");
    }

    // Store selected role
    const roleInput =
        document.getElementById("selectedRole");

    if (roleInput) {
        roleInput.value = role;
    }

    console.log("Selected role:", role);
}


/* -----------------------------------------
   HANDLE LOGIN
----------------------------------------- */

function handleLogin(event) {

    // Stop normal form submission
    event.preventDefault();

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value;

    const role =
        document.getElementById("selectedRole").value;

    const message =
        document.getElementById("loginMessage");


    // Basic validation
    if (!email || !password) {

        showLoginMessage(
            "Please enter your email and password.",
            "error"
        );

        return;
    }


    /*
        DEMO AUTHENTICATION

        Later this will be replaced with:
        Flask API → MySQL → Authentication

        For now we store demo login information
        in localStorage.
    */

    const user = {
        email: email,
        role: role
    };


    localStorage.setItem(
        "techSparkUser",
        JSON.stringify(user)
    );


    showLoginMessage(
        "Login successful. Redirecting...",
        "success"
    );


    // Redirect according to role
    setTimeout(() => {

        if (role === "admin") {

            window.location.href =
                "admin/dashboard.html";

        } else {

            window.location.href =
                "employee/dashboard.html";

        }

    }, 700);
}


/* -----------------------------------------
   DEMO LOGIN
----------------------------------------- */

function demoLogin() {

    const role =
        document.getElementById("selectedRole").value;


    let demoUser;


    if (role === "admin") {

        demoUser = {
            name: "Tech Spark Admin",
            email: "admin@techspark.demo",
            role: "admin"
        };

    } else {

        demoUser = {
            name: "Ruchitha",
            email: "employee@techspark.demo",
            role: "employee"
        };

    }


    // Save demo user
    localStorage.setItem(
        "techSparkUser",
        JSON.stringify(demoUser)
    );


    showLoginMessage(
        "Demo mode activated. Opening dashboard...",
        "success"
    );


    setTimeout(() => {

        if (role === "admin") {

            window.location.href =
                "admin/dashboard.html";

        } else {

            window.location.href =
                "employee/dashboard.html";

        }

    }, 700);
}


/* -----------------------------------------
   SHOW LOGIN MESSAGE
----------------------------------------- */

function showLoginMessage(text, type) {

    const message =
        document.getElementById("loginMessage");

    if (!message) {
        return;
    }

    message.textContent = text;

    message.className =
        "login-message-box " + type;
}


/* -----------------------------------------
   GET CURRENT USER
----------------------------------------- */

function getCurrentUser() {

    const storedUser =
        localStorage.getItem("techSparkUser");

    if (!storedUser) {
        return null;
    }

    try {

        return JSON.parse(storedUser);

    } catch (error) {

        console.error(
            "Unable to read user data:",
            error
        );

        return null;
    }
}


/* -----------------------------------------
   LOGOUT
----------------------------------------- */

function logout() {

    localStorage.removeItem("techSparkUser");

    window.location.href =
        "../login.html";
}


/* -----------------------------------------
   PROTECT DASHBOARD
----------------------------------------- */

function requireLogin(requiredRole = null) {

    const user = getCurrentUser();


    // User is not logged in
    if (!user) {

        window.location.href =
            "../login.html";

        return null;
    }


    // Check role
    if (
        requiredRole &&
        user.role !== requiredRole
    ) {

        alert(
            "You do not have permission to access this page."
        );

        window.location.href =
            "../login.html";

        return null;
    }


    return user;
}