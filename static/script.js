// Auto-fill URL 
const urlInput = document.getElementById("url");

if (urlInput) {
    urlInput.value = window.location.href;
}

// Smooth focus effect
const inputs = document.querySelectorAll("input, textarea");

inputs.forEach(input => {
    input.addEventListener("focus", () => {
        input.style.borderColor = "#3b82f6";
    });

    input.addEventListener("blur", () => {
        input.style.borderColor = "#1e293b";
    });
});