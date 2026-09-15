/* =========================================================
   TECH SPARK - LANDING PAGE JAVASCRIPT
   ========================================================= */

   document.addEventListener("DOMContentLoaded", () => {

    document.body.classList.add("page-ready");

    /* =====================================================
       NAVBAR SCROLL EFFECT
       ===================================================== */

    const navbar = document.querySelector(".navbar");

    function handleNavbar() {

        if (!navbar) return;

        if (window.scrollY > 30) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    }

    window.addEventListener("scroll", handleNavbar);

    handleNavbar();


    /* =====================================================
       SMOOTH SCROLL
       ===================================================== */

    const navigationLinks = document.querySelectorAll(
        'a[href^="#"]'
    );

    navigationLinks.forEach(link => {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });


    /* =====================================================
       ACTIVE NAVIGATION
       ===================================================== */

    const sections = document.querySelectorAll("section[id]");
    const navItems = document.querySelectorAll(".nav-links a");

    const sectionObserver = new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (!entry.isIntersecting) {
                    return;
                }

                const currentSection = entry.target.id;

                navItems.forEach(link => {

                    link.classList.remove("active");

                    const href = link.getAttribute("href");

                    if (href === `#${currentSection}`) {
                        link.classList.add("active");
                    }

                });

            });

        },
        {
            threshold: 0.35
        }
    );

    sections.forEach(section => {
        sectionObserver.observe(section);
    });


    /* =====================================================
       SCROLL REVEAL ANIMATION
       ===================================================== */

    const animatedElements = document.querySelectorAll(
        ".process-item, .process-step, .difference-card, .assistant-card, .impact-item, .hero-feature"
    );

    const revealObserver = new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("revealed");

                    revealObserver.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.15
        }
    );

    animatedElements.forEach((element, index) => {
        element.style.transitionDelay = `${Math.min(index * 55, 330)}ms`;
        revealObserver.observe(element);
    });


    /* =====================================================
       DASHBOARD HOVER EFFECT
       ===================================================== */

    const dashboard = document.querySelector(
        ".dashboard-window"
    );

    if (dashboard) {

        dashboard.addEventListener(
            "mousemove",
            event => {

                const rect = dashboard.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                const rotateY =
                    ((x / rect.width) - 0.5) * 3;

                const rotateX =
                    ((y / rect.height) - 0.5) * -3;

                dashboard.style.transform =
                    `perspective(1200px)
                     rotateX(${rotateX}deg)
                     rotateY(${rotateY}deg)`;

            }
        );

        dashboard.addEventListener(
            "mouseleave",
            () => {

                dashboard.style.transform =
                    "perspective(1200px) rotateX(0deg) rotateY(0deg)";

            }
        );

    }


    /* =====================================================
       ROBOT FLOATING ANIMATION
       ===================================================== */

    const robot = document.querySelector(
        ".hero-robot"
    );

    if (robot) {

        let direction = 1;
        let position = 0;

        function animateRobot() {

            position += 0.15 * direction;

            if (position > 6) {
                direction = -1;
            }

            if (position < -6) {
                direction = 1;
            }

            robot.style.transform =
                `translateX(-50%) translateY(${position}px)`;

            requestAnimationFrame(animateRobot);

        }

        animateRobot();

    }


    /* =====================================================
       LOADING DOT ANIMATION
       ===================================================== */

    const dots = document.querySelectorAll(
        ".loading-dots span"
    );

    dots.forEach((dot, index) => {

        dot.style.animation =
            `techSparkPulse 1.4s ${index * 0.2}s infinite`;

    });


    /* =====================================================
       ADD PULSE ANIMATION
       ===================================================== */

    const animationStyle = document.createElement("style");

    animationStyle.textContent = `

        @keyframes techSparkPulse {

            0%,
            100% {
                opacity: .25;
                transform: scale(.8);
            }

            50% {
                opacity: 1;
                transform: scale(1.15);
            }

        }

        .navbar {
            transition:
                background .3s ease,
                backdrop-filter .3s ease,
                padding .3s ease;
        }

        .navbar.scrolled {
            background: rgba(1, 22, 14, .88);
            backdrop-filter: blur(14px);
            padding-top: 12px;
            padding-bottom: 12px;
        }

        .process-step,
        .difference-card,
        .assistant-card,
        .impact-item {
            opacity: 0;
            transform: translateY(30px);
            transition:
                opacity .7s ease,
                transform .7s ease;
        }

        .process-step.revealed,
        .difference-card.revealed,
        .assistant-card.revealed,
        .impact-item.revealed {
            opacity: 1;
            transform: translateY(0);
        }

        .dashboard-window {
            transition:
                transform .25s ease,
                box-shadow .25s ease;
        }

        .dashboard-window:hover {
            box-shadow:
                0 35px 80px rgba(0, 0, 0, .45),
                0 0 50px rgba(50, 235, 150, .12);
        }

        .primary-btn,
        .secondary-btn,
        .signin-btn,
        .get-started {
            transition:
                transform .25s ease,
                box-shadow .25s ease,
                background .25s ease;
        }

        .primary-btn:hover,
        .secondary-btn:hover,
        .signin-btn:hover,
        .get-started:hover {
            transform: translateY(-2px);
        }

    `;

    document.head.appendChild(animationStyle);


    /* =====================================================
       INITIAL HASH SCROLL
       ===================================================== */

    if (window.location.hash) {

        const target = document.querySelector(
            window.location.hash
        );

        if (target) {

            setTimeout(() => {

                target.scrollIntoView({
                    behavior: "smooth"
                });

            }, 300);

        }

    }


    /* =====================================================
       CONSOLE MESSAGE
       ===================================================== */

    console.log(
        "%c Tech Spark ",
        "background:#42e99c;color:#03251a;font-weight:bold;padding:6px 10px;border-radius:5px;"
    );

    console.log(
        "AI-powered Competency Intelligence Platform"
    );

});