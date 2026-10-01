function toggleMenu() {
    const nav = document.getElementById("mainNav");
    if (!nav) return;
    nav.style.display = nav.style.display === "flex" ? "" : "flex";
}

document.addEventListener("DOMContentLoaded", () => {
    // Small confirmation for forms that can change important records.
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", event => {
            const button = form.querySelector("button[type='submit'], button:not([type])");
            if (button && button.dataset.loading === "true") return;
            if (button) {
                button.dataset.loading = "true";
                button.dataset.originalText = button.textContent;
                button.textContent = "Submitting...";
                setTimeout(() => {
                    button.dataset.loading = "false";
                    button.textContent = button.dataset.originalText;
                }, 4000);
            }
        });
    });
});
