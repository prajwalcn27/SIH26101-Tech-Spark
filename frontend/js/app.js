/* =========================================================
   TECH SPARK - AUTHENTICATION
   Employee / Admin Login
========================================================= */


/* =========================================================
   SELECT ROLE
========================================================= */

function selectRole(role) {

    // Remove active state from all role buttons
    const roleButtons = document.querySelectorAll(".role-option");

    roleButtons.forEach(function (button) {
        button.classList.remove("active");
    });


    // Add active state to selected role
    const selectedButton = document.querySelector(
        '.role-option[data-role="' + role + '"]'
    );

    if (selectedButton) {
        selectedButton.classList.add("active");
    }


    // Update hidden role field
    const selectedRole = document.getElementById("selectedRole");

    if (selectedRole) {
        selectedRole.value = role;
    }
}



/* =========================================================
   NORMAL LOGIN
========================================================= */

function handleLogin(event) {

    event.preventDefault();


    // Get form values
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const roleInput = document.getElementById("selectedRole");
    const rememberInput = document.getElementById("remember");


    if (!emailInput || !passwordInput || !roleInput) {
        return;
    }


    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const role = roleInput.value;


    // Basic validation
    if (!email) {

        showLoginMessage(
            "Please enter your email address.",
            "error"
        );

        emailInput.focus();

        return;
    }


    if (!password) {

        showLoginMessage(
            "Please enter your password.",
            "error"
        );

        passwordInput.focus();

        return;
    }


    // Validate email format
    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(email)) {

        showLoginMessage(
            "Please enter a valid email address.",
            "error"
        );

        emailInput.focus();

        return;
    }


    // Create temporary user object
    // Backend authentication can replace this later.
    const user = {

        email: email,

        role: role,

        name:
            role === "admin"
                ? "Admin User"
                : "Employee User",

        remember:
            rememberInput
                ? rememberInput.checked
                : false,

        loginTime:
            new Date().toISOString()

    };


    // Save login information
    localStorage.setItem(
        "currentUser",
        JSON.stringify(user)
    );


    // Show success message
    showLoginMessage(
        "Login successful. Redirecting...",
        "success"
    );


    // Redirect based on role
    setTimeout(function () {

        redirectByRole(role);

    }, 500);
}



/* =========================================================
   DEMO LOGIN
========================================================= */

function demoLogin() {

    const roleElement =
        document.getElementById("selectedRole");


    const role =
        roleElement
            ? roleElement.value
            : "employee";


    // Create demo user
    const demoUser = {

        email:
            role === "admin"
                ? "admin@techspark.demo"
                : "employee@techspark.demo",

        role: role,

        name:
            role === "admin"
                ? "Admin User"
                : "Employee User",

        demo: true,

        loginTime:
            new Date().toISOString()

    };


    // Save demo user
    localStorage.setItem(
        "currentUser",
        JSON.stringify(demoUser)
    );


    // Redirect
    redirectByRole(role);
}



/* =========================================================
   REDIRECT BASED ON ROLE
========================================================= */

function redirectByRole(role) {

    if (role === "admin") {

        window.location.href =
            "admin/dashboard.html";

    } else {

        window.location.href =
            "employee/dashboard.html";

    }
}



/* =========================================================
   SHOW LOGIN MESSAGE
========================================================= */

function showLoginMessage(message, type) {

    const box =
        document.getElementById("loginMessage");


    if (!box) {
        return;
    }


    box.textContent = message;


    // Reset classes
    box.className =
        "login-message-box " + type;


    // Automatically remove message after a few seconds
    setTimeout(function () {

        if (box) {

            box.textContent = "";
            box.className = "login-message-box";

        }

    }, 4000);
}



/* =========================================================
   GET CURRENT USER
========================================================= */

function getCurrentUser() {

    const user =
        localStorage.getItem("currentUser");


    if (!user) {
        return null;
    }


    try {

        return JSON.parse(user);

    } catch (error) {

        console.error(
            "Invalid user data:",
            error
        );

        localStorage.removeItem("currentUser");

        return null;
    }
}



/* =========================================================
   CHECK LOGIN
========================================================= */

function isLoggedIn() {

    const user = getCurrentUser();

    return user !== null;
}



/* =========================================================
   REQUIRE LOGIN
========================================================= */

function requireLogin(requiredRole) {

    const user = getCurrentUser();


    // User is not logged in
    if (!user) {

        window.location.href =
            "../../pages/login.html";

        return false;
    }


    // Check required role
    if (
        requiredRole &&
        user.role !== requiredRole
    ) {

        alert(
            "Unauthorized access.\n\n" +
            "This page is available only for " +
            requiredRole + " users."
        );


        // Redirect to correct dashboard
        if (user.role === "admin") {

            window.location.href =
                "../../pages/admin/dashboard.html";

        } else {

            window.location.href =
                "../../pages/employee/dashboard.html";

        }


        return false;
    }


    return true;
}



/* =========================================================
   LOGOUT
========================================================= */

function logout() {

    // Remove current user
    localStorage.removeItem("currentUser");


    // Redirect to login page
    window.location.href =
        "../../pages/login.html";
}



/* =========================================================
   GET USER NAME
========================================================= */

function getUserName() {

    const user = getCurrentUser();


    if (!user) {
        return "User";
    }


    return user.name || "User";
}



/* =========================================================
   GET USER EMAIL
========================================================= */

function getUserEmail() {

    const user = getCurrentUser();


    if (!user) {
        return "";
    }


    return user.email || "";
}



/* =========================================================
   GET USER ROLE
========================================================= */

function getUserRole() {

    const user = getCurrentUser();


    if (!user) {
        return "";
    }


    return user.role || "";
}



/* =========================================================
   DISPLAY USER INFORMATION
========================================================= */

function loadUserInformation() {

    const user = getCurrentUser();


    if (!user) {
        return;
    }


    // User name
    const nameElements =
        document.querySelectorAll(
            "[data-user-name]"
        );


    nameElements.forEach(function (element) {

        element.textContent =
            user.name || "User";

    });


    // User email
    const emailElements =
        document.querySelectorAll(
            "[data-user-email]"
        );


    emailElements.forEach(function (element) {

        element.textContent =
            user.email || "";

    });


    // User role
    const roleElements =
        document.querySelectorAll(
            "[data-user-role]"
        );


    roleElements.forEach(function (element) {

        element.textContent =
            user.role || "";

    });
}



/* =========================================================
   LOGIN PAGE INITIALIZATION
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Default role = employee
        const selectedRole =
            document.getElementById(
                "selectedRole"
            );


        if (selectedRole) {

            if (!selectedRole.value) {

                selectedRole.value =
                    "employee";

            }

            selectRole(
                selectedRole.value
            );
        }


        // Load user information if dashboard
        loadUserInformation();

    }
);