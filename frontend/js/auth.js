/* =========================================================
   TECH SPARK - AUTHENTICATION JAVASCRIPT
   SIH26101 - Smart India Hackathon 2026
========================================================= */


/* =========================================================
   ROLE SELECTION
========================================================= */

function selectRole(role) {

    const roleButtons =
        document.querySelectorAll(".role-option");

    const selectedRole =
        document.getElementById("selectedRole");


    /*
     * Update active button
     */
    roleButtons.forEach(function (button) {

        button.classList.remove("active");

        if (button.dataset.role === role) {
            button.classList.add("active");
        }

    });


    /*
     * Store selected role
     */
    if (selectedRole) {
        selectedRole.value = role;
    }


    /*
     * Store temporarily
     */
    sessionStorage.setItem(
        "selectedRole",
        role
    );

}


/* =========================================================
   LOGIN FORM
========================================================= */

function handleLogin(event) {

    event.preventDefault();


    const emailInput =
        document.getElementById("email");

    const passwordInput =
        document.getElementById("password");

    const selectedRoleInput =
        document.getElementById("selectedRole");


    if (!emailInput || !passwordInput) {
        return;
    }


    const email =
        emailInput.value.trim();

    const password =
        passwordInput.value;

    const role =
        selectedRoleInput
            ? selectedRoleInput.value
            : "employee";


    /* -----------------------------------------------------
       Basic validation
    ----------------------------------------------------- */

    if (!email) {

        showLoginMessage(
            "Please enter your email address.",
            "error"
        );

        emailInput.focus();

        return;
    }


    if (!isValidEmail(email)) {

        showLoginMessage(
            "Please enter a valid email address.",
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


    if (password.length < 4) {

        showLoginMessage(
            "Password must contain at least 4 characters.",
            "error"
        );

        passwordInput.focus();

        return;
    }


    /*
     * Show loading state
     */
    const loginButton =
        document.querySelector(".login-button");


    if (loginButton) {

        loginButton.disabled = true;

        loginButton.classList.add("loading");

        const buttonText =
            loginButton.querySelector("span:first-child");

        if (buttonText) {
            buttonText.textContent = "Signing in...";
        }

    }


    /*
     * Demo frontend authentication
     *
     * This will later be replaced with
     * Flask + MySQL authentication.
     */
    setTimeout(function () {

        const userName =
            getNameFromEmail(email);


        const user = {

            name: userName,

            email: email,

            role: role,

            loginTime: new Date().toISOString(),

            remember:
                document.getElementById("remember")
                    ? document.getElementById("remember").checked
                    : false

        };


        /*
         * Save current user
         */
        localStorage.setItem(
            "currentUser",
            JSON.stringify(user)
        );


        /*
         * Save role
         */
        localStorage.setItem(
            "userRole",
            role
        );


        /*
         * Show success
         */
        showLoginMessage(
            "Login successful. Redirecting...",
            "success"
        );


        /*
         * Redirect
         */
        setTimeout(function () {

            redirectByRole(role);

        }, 600);


    }, 700);

}


/* =========================================================
   DEMO LOGIN
========================================================= */

function demoLogin() {

    /*
     * Find selected role
     */
    const selectedRole =
        document.getElementById("selectedRole");


    const role =
        selectedRole
            ? selectedRole.value
            : "employee";


    /*
     * Demo accounts
     */
    let user;


    if (role === "admin") {

        user = {

            name: "System Administrator",

            email: "admin@techspark.gov.in",

            role: "admin",

            loginTime: new Date().toISOString(),

            demo: true

        };

    } else {

        user = {

            name: "Demo Employee",

            email: "employee@techspark.gov.in",

            role: "employee",

            loginTime: new Date().toISOString(),

            demo: true

        };

    }


    /*
     * Save demo user
     */
    localStorage.setItem(
        "currentUser",
        JSON.stringify(user)
    );


    localStorage.setItem(
        "userRole",
        role
    );


    /*
     * Show message
     */
    showLoginMessage(
        "Demo mode activated. Redirecting...",
        "success"
    );


    /*
     * Redirect
     */
    setTimeout(function () {

        redirectByRole(role);

    }, 500);

}


/* =========================================================
   REDIRECT BASED ON ROLE
========================================================= */

function redirectByRole(role) {

    if (role === "admin") {

        window.location.href =
            "admin/dashboard.html";

        return;

    }


    if (role === "employee") {

        window.location.href =
            "employee/dashboard.html";

        return;

    }


    /*
     * Default
     */
    window.location.href =
        "../index.html";

}


/* =========================================================
   LOGIN MESSAGE
========================================================= */

function showLoginMessage(message, type) {

    const messageBox =
        document.getElementById("loginMessage");


    if (!messageBox) {
        return;
    }


    messageBox.textContent =
        message;


    messageBox.className =
        "login-message-box " + type;


    messageBox.style.display =
        "block";


    /*
     * Auto hide error messages
     */
    if (type === "error") {

        setTimeout(function () {

            messageBox.style.display =
                "none";

        }, 4000);

    }

}


/* =========================================================
   EMAIL VALIDATION
========================================================= */

function isValidEmail(email) {

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return emailPattern.test(email);

}


/* =========================================================
   GET NAME FROM EMAIL
========================================================= */

function getNameFromEmail(email) {

    const username =
        email.split("@")[0];


    if (!username) {
        return "User";
    }


    /*
     * Convert:
     * prajwal.cn
     *
     * to:
     * Prajwal Cn
     */
    return username
        .replace(/[._-]+/g, " ")
        .replace(/\b\w/g, function (letter) {
            return letter.toUpperCase();
        });

}


/* =========================================================
   GET CURRENT USER
========================================================= */

function getCurrentUser() {

    const userData =
        localStorage.getItem("currentUser");


    if (!userData) {
        return null;
    }


    try {

        return JSON.parse(userData);

    } catch (error) {

        console.error(
            "Unable to read current user:",
            error
        );

        localStorage.removeItem(
            "currentUser"
        );

        return null;

    }

}


/* =========================================================
   CHECK LOGIN STATUS
========================================================= */

function isLoggedIn() {

    const user =
        getCurrentUser();

    return user !== null;

}


/* =========================================================
   GET USER ROLE
========================================================= */

function getUserRole() {

    const user =
        getCurrentUser();


    if (!user) {
        return null;
    }


    return user.role || null;

}


/* =========================================================
   GET USER NAME
========================================================= */

function getUserName() {

    const user =
        getCurrentUser();


    if (!user) {
        return "User";
    }


    return user.name || "User";

}


/* =========================================================
   GET USER EMAIL
========================================================= */

function getUserEmail() {

    const user =
        getCurrentUser();


    if (!user) {
        return "";

    }


    return user.email || "";

}


/* =========================================================
   REQUIRE LOGIN
========================================================= */

function requireLogin(requiredRole) {

    const user =
        getCurrentUser();


    /*
     * No user logged in
     */
    if (!user) {

        window.location.href =
            "../login.html";

        return false;

    }


    /*
     * Check role
     */
    if (
        requiredRole &&
        user.role !== requiredRole
    ) {

        /*
         * Employee trying to access admin
         * or admin trying to access employee
         */
        redirectByRole(user.role);

        return false;

    }


    return true;

}


/* =========================================================
   LOGOUT
========================================================= */

function logout() {

    /*
     * Remove authentication data
     */
    localStorage.removeItem(
        "currentUser"
    );

    localStorage.removeItem(
        "userRole"
    );


    sessionStorage.removeItem(
        "selectedRole"
    );


    /*
     * Redirect to login
     */
    window.location.href =
        "../login.html";

}


/* =========================================================
   LOAD USER INFORMATION
========================================================= */

function loadUserInformation() {

    const user =
        getCurrentUser();


    if (!user) {
        return;
    }


    /*
     * User name
     */
    document
        .querySelectorAll("[data-user-name]")
        .forEach(function (element) {

            element.textContent =
                user.name || "User";

        });


    /*
     * User email
     */
    document
        .querySelectorAll("[data-user-email]")
        .forEach(function (element) {

            element.textContent =
                user.email || "";

        });


    /*
     * User role
     */
    document
        .querySelectorAll("[data-user-role]")
        .forEach(function (element) {

            if (user.role === "admin") {

                element.textContent =
                    "System Administrator";

            } else {

                element.textContent =
                    "Employee";

            }

        });


    /*
     * User avatar
     */
    document
        .querySelectorAll("[data-user-avatar]")
        .forEach(function (element) {

            element.textContent =
                getInitials(user.name);

        });

}


/* =========================================================
   GET USER INITIALS
========================================================= */

function getInitials(name) {

    if (!name) {
        return "U";
    }


    const words =
        name.trim().split(/\s+/);


    if (words.length === 1) {

        return words[0]
            .substring(0, 2)
            .toUpperCase();

    }


    return (
        words[0].charAt(0) +
        words[words.length - 1].charAt(0)
    ).toUpperCase();

}


/* =========================================================
   RESTORE SELECTED ROLE
========================================================= */

function restoreSelectedRole() {

    const savedRole =
        sessionStorage.getItem(
            "selectedRole"
        );


    if (!savedRole) {
        return;
    }


    const roleInput =
        document.getElementById(
            "selectedRole"
        );


    if (roleInput) {

        roleInput.value =
            savedRole;

    }


    const roleButtons =
        document.querySelectorAll(
            ".role-option"
        );


    roleButtons.forEach(function (button) {

        button.classList.remove("active");


        if (
            button.dataset.role ===
            savedRole
        ) {

            button.classList.add("active");

        }

    });

}


/* =========================================================
   PASSWORD VISIBILITY
========================================================= */

function togglePassword() {

    const password =
        document.getElementById("password");


    if (!password) {
        return;
    }


    if (password.type === "password") {

        password.type = "text";

    } else {

        password.type = "password";

    }

}


/* =========================================================
   AUTO INITIALIZATION
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
         * Load user information
         */
        loadUserInformation();


        /*
         * Restore selected login role
         */
        restoreSelectedRole();


        /*
         * Add password toggle if
         * a toggle button exists
         */
        const passwordToggle =
            document.querySelector(
                "[data-password-toggle]"
            );


        if (passwordToggle) {

            passwordToggle.addEventListener(
                "click",
                togglePassword
            );

        }


        /*
         * Enter key support
         */
        const passwordInput =
            document.getElementById(
                "password"
            );


        if (passwordInput) {

            passwordInput.addEventListener(
                "keydown",
                function (event) {

                    if (event.key === "Enter") {

                        const form =
                            document.getElementById(
                                "loginForm"
                            );


                        if (form) {

                            /*
                             * requestSubmit triggers
                             * normal form validation
                             */
                            if (
                                typeof form.requestSubmit ===
                                "function"
                            ) {

                                form.requestSubmit();

                            }

                        }

                    }

                }
            );

        }

    }
);