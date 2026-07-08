// ==========================================
// SUMMARAI PRO
// THEME MANAGER
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    const root = document.documentElement;

    const themeSelect = document.querySelector(
        'select[name="theme"]'
    );

    // Load saved theme

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {

        applyTheme(savedTheme);

        if (themeSelect) {

            themeSelect.value = savedTheme;

        }

    }

    // Save theme when changed

    if (themeSelect) {

        themeSelect.addEventListener("change", function () {

            const theme = this.value;

            localStorage.setItem(
                "theme",
                theme
            );

            applyTheme(theme);

        });

    }

    function applyTheme(theme) {

        if (theme === "light") {

            root.style.setProperty(
                "--background",
                "#F4F7FC"
            );

            root.style.setProperty(
                "--surface",
                "#FFFFFF"
            );

            root.style.setProperty(
                "--surface-light",
                "#EEF2F7"
            );

            root.style.setProperty(
                "--text",
                "#1F2937"
            );

            root.style.setProperty(
                "--text-light",
                "#6B7280"
            );

            document.body.style.background =
                "#F4F7FC";

        }

        else {

            root.style.setProperty(
                "--background",
                "#0F172A"
            );

            root.style.setProperty(
                "--surface",
                "#182338"
            );

            root.style.setProperty(
                "--surface-light",
                "#24324B"
            );

            root.style.setProperty(
                "--text",
                "#FFFFFF"
            );

            root.style.setProperty(
                "--text-light",
                "#C7D2FE"
            );

            document.body.style.background =
                "linear-gradient(135deg,#0F172A,#16213E,#1D3557)";

        }

    }

});