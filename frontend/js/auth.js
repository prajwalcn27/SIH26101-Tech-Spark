/* =========================================================
   TECH SPARK
   AUTHENTICATION JAVASCRIPT
   ========================================================= */


/* =========================================================
   1. ROLE SELECTION
   ========================================================= */

   function selectRole(role) {

    const normalizedRole = role === "admin" ? "admin" : "employee";
    const page = document.body;

    if (page) {
        page.dataset.roleMode = normalizedRole;
    }

    const roleInput =
        document.getElementById("selectedRole");

    if (roleInput) {
        roleInput.value = normalizedRole;
    }


    /*
     * Remove active state from all role cards
     */

    const roleCards =
        document.querySelectorAll(
            ".role-option"
        );

    roleCards.forEach(function (card) {

        card.classList.remove("active");

    });


    /*
     * Find selected role card
     */

    const selectedCard =
        document.querySelector(
            '[data-role="' + normalizedRole + '"]'
        );

    if (selectedCard) {

        selectedCard.classList.add(
            "active"
        );

    }


    /*
     * Update visible role text
     */

    const roleText =
        document.getElementById(
            "selectedRoleText"
        );

    if (roleText) {

        if (normalizedRole === "admin") {

            roleText.textContent =
                "Administrator";

        } else {

            roleText.textContent =
                "Employee";

        }

    }

    const networkLabel = document.getElementById("networkLabel");
    const networkCaption = document.getElementById("networkCaption");
    const modeDescription = document.getElementById("loginModeDescription");

    if (networkLabel) {
        networkLabel.textContent = normalizedRole === "admin"
            ? "COMMAND NETWORK"
            : "LEARNING NETWORK";
    }

    if (networkCaption) {
        networkCaption.textContent = normalizedRole === "admin"
            ? "People · skills · gaps · insight"
            : "Assess · analyse · learn · improve";
    }

    if (modeDescription) {
        modeDescription.textContent = normalizedRole === "admin"
            ? "Enter the command center for organization-wide competency intelligence."
            : "Continue your personalized learning journey.";
    }

}


/* =========================================================
   2. LOGIN
   ========================================================= */

async function handleLogin(event) {

    /*
     * Prevent normal form submission
     */

    if (event) {
        event.preventDefault();
    }


    /*
     * Get form elements
     */

    const emailInput =
        document.getElementById("email");

    const passwordInput =
        document.getElementById("password");

    const roleInput =
        document.getElementById("selectedRole");


    /*
     * Get values safely
     */

    const email =
        emailInput
            ? emailInput.value.trim()
            : "";

    const password =
        passwordInput
            ? passwordInput.value.trim()
            : "";

    const selectedRole =
        roleInput
            ? roleInput.value
            : "employee";

    const submitButton =
        document.getElementById("loginSubmitButton");


    /*
     * Validate email
     */

    if (!email) {

        showLoginMessage(
            "Please enter your email address.",
            "error"
        );

        if (emailInput) {
            emailInput.focus();
        }

        return false;
    }


    /*
     * Validate email format
     */

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {

        showLoginMessage(
            "Please enter a valid email address.",
            "error"
        );

        if (emailInput) {
            emailInput.focus();
        }

        return false;
    }


    /*
     * Validate password
     */

    if (!password) {

        showLoginMessage(
            "Please enter your password.",
            "error"
        );

        if (passwordInput) {
            passwordInput.focus();
        }

        return false;
    }


    /*
     * Minimum password validation
     */

    if (password.length < 4) {

        showLoginMessage(
            "Password must contain at least 4 characters.",
            "error"
        );

        if (passwordInput) {
            passwordInput.focus();
        }

        return false;
    }


    let user;

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.classList.add("is-loading");
        submitButton.querySelector("span:first-child").textContent = "Signing in...";
    }

    try {

        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const payload = await response.json();

        if (!response.ok || !payload.success || !payload.user) {
            throw new Error(payload.message || "Unable to sign in.");
        }

        user = payload.user;

        if (user.role !== selectedRole) {
            throw new Error(
                "This account does not have access to the selected role."
            );
        }

        user.loginTime = new Date().toISOString();

    } catch (error) {

        showLoginMessage(
            error.message === "This account does not have access to the selected role."
                ? error.message
                : "Unable to sign in. Please check your email and password.",
            "error"
        );
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.classList.remove("is-loading");
            submitButton.querySelector("span:first-child").textContent = "Sign in";
        }
        return false;
    }


    /*
     * Save login session
     */

    try {

        localStorage.setItem(
            "techSparkUser",
            JSON.stringify(user)
        );

        localStorage.setItem(
            "isLoggedIn",
            "true"
        );

    } catch (error) {

        console.error(
            "Unable to save login session:",
            error
        );

        showLoginMessage(
            "Unable to save login session. Please check browser storage.",
            "error"
        );

        return false;

    }


    /*
     * Show success message
     */

    showLoginMessage(
        "Authentication successful. Redirecting...",
        "success"
    );


    /*
     * Redirect
     */

    setTimeout(
        function () {

            redirectByRole(
                user.role
            );

        },
        500
    );


    return false;
}


/* =========================================================
   3. DEMO LOGIN
   ========================================================= */

function demoLogin(role) {

    const roleInput = document.getElementById("selectedRole");

    if (roleInput) {
        roleInput.value = role === "admin" ? "admin" : "employee";
    }

    showLoginMessage(
        "Demo access is disabled. Sign in with a registered account.",
        "error"
    );

    return false;

}


/* =========================================================
   4. REDIRECT BY ROLE
   ========================================================= */

function redirectByRole(role) {

    /*
     * Normalize role
     */

    role =
        String(role || "")
            .toLowerCase()
            .trim();


    /*
     * Determine current page
     */

    const currentPath =
        window.location.pathname
            .replace(/\\/g, "/");


    /*
     * Admin dashboard
     */

    if (role === "admin") {

        if (
            currentPath.includes(
                "/pages/login.html"
            ) ||
            currentPath.endsWith(
                "/index.html"
            ) ||
            currentPath === "/"
        ) {

            window.location.href =
                "admin/dashboard.html";

            return;

        }


        /*
         * If already inside pages,
         * use relative admin path.
         */

        if (
            currentPath.includes(
                "/pages/"
            )
        ) {

            window.location.href =
                "admin/dashboard.html";

            return;

        }


        window.location.href =
            "pages/admin/dashboard.html";

        return;

    }


    /*
     * Employee dashboard
     */

    if (
        currentPath.includes(
            "/pages/login.html"
        ) ||
        currentPath.endsWith(
            "/index.html"
        ) ||
        currentPath === "/"
    ) {

        window.location.href =
            "employee/dashboard.html";

        return;

    }


    if (
        currentPath.includes(
            "/pages/"
        )
    ) {

        window.location.href =
            "employee/dashboard.html";

        return;

    }


    window.location.href =
        "pages/employee/dashboard.html";

}


/* =========================================================
   5. LOGIN MESSAGE
   ========================================================= */

function showLoginMessage(
    message,
    type
) {

    /*
     * Try existing message container
     */

    let messageElement =
        document.getElementById(
            "loginMessage"
        );


    /*
     * If it does not exist,
     * create one.
     */

    if (!messageElement) {

        messageElement =
            document.createElement(
                "div"
            );

        messageElement.id =
            "loginMessage";

        const form =
            document.querySelector(
                "form"
            );

        if (form) {

            form.prepend(
                messageElement
            );

        } else {

            document.body.prepend(
                messageElement
            );

        }

    }


    /*
     * Set message
     */

    messageElement.textContent =
        message;


    /*
     * Set message type
     */

    messageElement.className =
        "login-message " +
        (type || "info");


    /*
     * Automatically remove
     * temporary message
     */

    if (
        type === "success" ||
        type === "error"
    ) {

        setTimeout(
            function () {

                if (
                    messageElement &&
                    messageElement.parentNode
                ) {

                    messageElement.classList.add(
                        "message-hidden"
                    );

                }

            },
            4000
        );

    }

}


/* =========================================================
   6. GET CURRENT USER
   ========================================================= */

function getCurrentUser() {

    try {

        const storedUser =
            localStorage.getItem(
                "techSparkUser"
            );

        if (!storedUser) {
            return null;
        }

        const user =
            JSON.parse(
                storedUser
            );

        if (
            !user ||
            typeof user !== "object"
        ) {
            return null;
        }

        return user;

    } catch (error) {

        console.error(
            "Unable to read current user:",
            error
        );

        return null;

    }

}

async function syncCurrentUserFromServer() {
    try {
        const response = await fetch("/api/session", {
            method: "GET",
            credentials: "same-origin"
        });

        if (!response.ok) {
            localStorage.removeItem("techSparkUser");
            localStorage.removeItem("isLoggedIn");
            return null;
        }

        const payload = await response.json();

        if (!payload || !payload.success || !payload.user) {
            localStorage.removeItem("techSparkUser");
            localStorage.removeItem("isLoggedIn");
            return null;
        }

        const user = payload.user;
        localStorage.setItem("techSparkUser", JSON.stringify(user));
        localStorage.setItem("isLoggedIn", "true");
        return user;
    } catch (error) {
        console.warn("Unable to sync user session from server:", error);
        return getCurrentUser();
    }
}


/* =========================================================
   7. CHECK LOGIN
   ========================================================= */

async function isLoggedIn() {

    const serverUser = await syncCurrentUserFromServer();

    if (serverUser) {
        return true;
    }

    const user =
        getCurrentUser();

    const loginFlag =
        localStorage.getItem(
            "isLoggedIn"
        );


    return (
        loginFlag === "true" &&
        user !== null
    );

}


/* =========================================================
   8. REQUIRE LOGIN
   ========================================================= */

async function requireLogin(
    requiredRole
) {

    const serverUser = await syncCurrentUserFromServer();
    const user = serverUser || getCurrentUser();

    if (!user) {
        redirectToLogin();
        return false;
    }

    if (!requiredRole) {
        return true;
    }

    const actualRole =
        String(
            user.role || ""
        )
            .toLowerCase()
            .trim();

    const expectedRole =
        String(
            requiredRole
        )
            .toLowerCase()
            .trim();

    if (
        actualRole !== expectedRole
    ) {
        redirectByRole(
            actualRole
        );
        return false;
    }

    return true;

}


/* =========================================================
   9. REDIRECT TO LOGIN
   ========================================================= */

function redirectToLogin() {

    const path =
        window.location.pathname
            .replace(/\\/g, "/");


    /*
     * Dashboard pages
     */

    if (
        path.includes(
            "/pages/admin/"
        ) ||
        path.includes(
            "/pages/employee/"
        )
    ) {

        window.location.href =
            "../login.html";

        return;

    }


    /*
     * Already inside pages
     */

    if (
        path.includes(
            "/pages/"
        )
    ) {

        window.location.href =
            "login.html";

        return;

    }


    /*
     * Root frontend
     */

    window.location.href =
        "pages/login.html";

}


/* =========================================================
   10. LOGOUT
   ========================================================= */

async function logout() {

    try {
        await fetch("/api/logout", { method: "POST" });
    } catch (error) {
        console.warn("Server logout could not be completed:", error);
    }

    try {

        localStorage.removeItem(
            "techSparkUser"
        );

        localStorage.removeItem(
            "isLoggedIn"
        );

        /*
         * Remove any temporary
         * authentication data.
         */

        sessionStorage.clear();

    } catch (error) {

        console.error(
            "Logout error:",
            error
        );

    }


    /*
     * Redirect to login page
     */

    const path =
        window.location.pathname
            .replace(/\\/g, "/");


    if (
        path.includes(
            "/pages/admin/"
        ) ||
        path.includes(
            "/pages/employee/"
        )
    ) {

        window.location.href =
            "../login.html";

        return;

    }


    if (
        path.includes(
            "/pages/"
        )
    ) {

        window.location.href =
            "login.html";

        return;

    }


    window.location.href =
        "pages/login.html";

}


/* =========================================================
   11. GET USER NAME
   ========================================================= */

function getUserName() {

    const user =
        getCurrentUser();

    if (!user) {
        return "";
    }

    return user.name || "";

}


/* =========================================================
   12. GET USER EMAIL
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
   13. GET USER ROLE
   ========================================================= */

function getUserRole() {

    const user =
        getCurrentUser();

    if (!user) {
        return "";
    }

    return user.role || "";

}


/* =========================================================
   14. CREATE USER NAME
   ========================================================= */

function createUserName(
    email
) {

    if (!email) {
        return "Tech Spark User";
    }


    const username =
        email
            .split("@")[0]
            .replace(/[._-]+/g, " ")
            .trim();


    if (!username) {
        return "Tech Spark User";
    }


    return username
        .split(" ")
        .map(function (word) {

            if (!word) {
                return "";
            }

            return (
                word
                    .charAt(0)
                    .toUpperCase() +
                word
                    .slice(1)
                    .toLowerCase()
            );

        })
        .join(" ");

}


/* =========================================================
   15. LOAD USER INFORMATION
   ========================================================= */

function loadUserInformation() {

    const user =
        getCurrentUser();


    if (!user) {
        return;
    }


    /*
     * Possible name elements
     */

    const nameElements =
        document.querySelectorAll(
            "[data-user-name]"
        );

    nameElements.forEach(
        function (element) {

            element.textContent =
                user.name || "User";

        }
    );


    /*
     * Possible email elements
     */

    const emailElements =
        document.querySelectorAll(
            "[data-user-email]"
        );

    emailElements.forEach(
        function (element) {

            element.textContent =
                user.email || "";

        }
    );


    /*
     * Possible role elements
     */

    const roleElements =
        document.querySelectorAll(
            "[data-user-role]"
        );

    roleElements.forEach(
        function (element) {

            element.textContent =
                user.role === "admin"
                    ? "Administrator"
                    : "Employee";

        }
    );


    /*
     * Common IDs
     */

    const userName =
        document.getElementById(
            "userName"
        );

    if (userName) {

        userName.textContent =
            user.name || "User";

    }


    const userEmail =
        document.getElementById(
            "userEmail"
        );

    if (userEmail) {

        userEmail.textContent =
            user.email || "";

    }


    const userRole =
        document.getElementById(
            "userRole"
        );

    if (userRole) {

        userRole.textContent =
            user.role === "admin"
                ? "Administrator"
                : "Employee";

    }

}


/* =========================================================
   16. INITIALIZE AUTH PAGE
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
         * Load current user information
         * if this page contains user fields.
         */

        loadUserInformation();


        /*
         * Login form
         */

        const loginForm =
            document.getElementById(
                "loginForm"
            );


        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                handleLogin
            );

        }

        const passwordToggle = document.getElementById("passwordToggle");
        const passwordInput = document.getElementById("password");

        if (passwordToggle && passwordInput) {
            passwordToggle.addEventListener("click", function () {
                const showing = passwordInput.type === "text";
                passwordInput.type = showing ? "password" : "text";
                passwordToggle.setAttribute("aria-pressed", String(!showing));
                passwordToggle.setAttribute("aria-label", showing ? "Show password" : "Hide password");
            });
        }


        /*
         * Logout buttons
         */

        const logoutButtons =
            document.querySelectorAll(
                '[data-action="logout"], ' +
                ".logout-btn, " +
                "#logoutBtn"
            );


        logoutButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function (event) {

                        event.preventDefault();

                        logout();

                    }
                );

            }
        );

    }
);


/* =========================================================
   17. EXPORT FUNCTIONS TO WINDOW
   ========================================================= */

window.selectRole =
    selectRole;

window.handleLogin =
    handleLogin;

window.demoLogin =
    demoLogin;

window.redirectByRole =
    redirectByRole;

window.showLoginMessage =
    showLoginMessage;

window.getCurrentUser =
    getCurrentUser;

window.isLoggedIn =
    isLoggedIn;

window.requireLogin =
    requireLogin;

window.logout =
    logout;

window.getUserName =
    getUserName;

window.getUserEmail =
    getUserEmail;

window.getUserRole =
    getUserRole;

window.loadUserInformation =
    loadUserInformation;
