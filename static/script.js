const text = document.getElementById("text");
const wordCount = document.getElementById("wordCount");
const charCount = document.getElementById("charCount");

function updateCounter() {

    const value = text.value.trim();

    charCount.innerText = value.length;

    if (value === "") {
        wordCount.innerText = "0";
    } else {
        wordCount.innerText = value.split(/\s+/).length;
    }
}

text.addEventListener("input", updateCounter);

window.onload = updateCounter;

function clearText() {

    document.getElementById("text").value = "";
    document.getElementById("summaryText").value = "";

    wordCount.innerText = "0";
    charCount.innerText = "0";
}

function copySummary() {

    const summary = document.getElementById("summaryText");

    if (summary.value.trim() === "") {
        alert("No summary available!");
        return;
    }

    summary.select();
    summary.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(summary.value);

    alert("Summary copied successfully!");
}