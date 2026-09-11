/* =========================================================
   TECH SPARK - ADMIN JAVASCRIPT
   SIH26101 | Admin Dashboard
   ========================================================= */


/* =========================================================
   MATERIAL UPLOAD
   ========================================================= */

   function handleMaterialUpload() {

    const fileInput = document.getElementById("materialFile");

    if (!fileInput) {
        return;
    }

    if (fileInput.files.length === 0) {

        alert("Please select a PDF, PPT, or DOCX file.");

        return;
    }

    const file = fileInput.files[0];

    const allowedExtensions = [
        ".pdf",
        ".ppt",
        ".pptx",
        ".doc",
        ".docx"
    ];

    const fileName = file.name.toLowerCase();

    const validFile = allowedExtensions.some(function (extension) {

        return fileName.endsWith(extension);

    });

    if (!validFile) {

        alert(
            "Invalid file format.\n\n" +
            "Please upload PDF, PPT, PPTX, DOC, or DOCX."
        );

        fileInput.value = "";

        return;
    }


    /* File size check */

    const maxSize = 25 * 1024 * 1024;

    if (file.size > maxSize) {

        alert(
            "File is too large.\n\n" +
            "Maximum allowed size is 25 MB."
        );

        fileInput.value = "";

        return;
    }


    /* Demo upload message */

    alert(
        "Learning material selected successfully!\n\n" +
        "File: " + file.name +
        "\n\n" +
        "The Flask backend will handle actual upload, " +
        "document extraction and AI processing."
    );

}


/* =========================================================
   APPROVE AI QUESTION
   ========================================================= */

function approveQuestion(button) {

    const row = button.closest("tr");

    if (!row) {
        return;
    }

    const question = row.querySelector(".question-cell");

    const flagButton = row.querySelector(".flag-btn");

    button.textContent = "Approved";

    button.disabled = true;

    button.style.opacity = "0.6";


    if (flagButton) {

        flagButton.disabled = true;

        flagButton.style.opacity = "0.5";

    }


    if (question) {

        question.style.opacity = "0.65";

    }

}


/* =========================================================
   FLAG AI QUESTION
   ========================================================= */

function flagQuestion(button) {

    const row = button.closest("tr");

    if (!row) {
        return;
    }

    const validation = row.querySelector(".validation");

    button.textContent = "Flagged";

    button.disabled = true;

    button.style.opacity = "0.6";


    if (validation) {

        validation.textContent = "⚠ Flagged";

        validation.style.color = "#b91c1c";

    }

}


/* =========================================================
   SMOOTH SCROLL
   ========================================================= */

function scrollToSection(sectionId) {

    const section = document.getElementById(sectionId);

    if (!section) {
        return;
    }

    section.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =========================================================
   INITIALIZE ADMIN DASHBOARD
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const fileInput =
        document.getElementById("materialFile");


    if (fileInput) {

        fileInput.addEventListener(
            "change",
            handleMaterialUpload
        );

    }

});
