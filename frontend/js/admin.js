/* =========================================================
   TECH SPARK - ADMIN JAVASCRIPT
   SIH26101 | Competency Intelligence Platform
   ========================================================= */


/* =========================================================
   GLOBAL SETTINGS
   ========================================================= */

   const MAX_FILE_SIZE = 25 * 1024 * 1024;

   const ALLOWED_EXTENSIONS = [
       ".pdf",
       ".ppt",
       ".pptx",
       ".doc",
       ".docx"
   ];
   
   
   /* =========================================================
      GET FILE EXTENSION
      ========================================================= */
   
   function getFileExtension(filename) {
   
       if (!filename) {
           return "";
       }
   
       const parts = filename.split(".");
   
       if (parts.length < 2) {
           return "";
       }
   
       return "." + parts.pop().toLowerCase();
   }
   
   
   /* =========================================================
      FORMAT FILE SIZE
      ========================================================= */
   
   function formatFileSize(bytes) {
   
       if (!bytes || bytes === 0) {
           return "0 Bytes";
       }
   
       const units = [
           "Bytes",
           "KB",
           "MB",
           "GB"
       ];
   
       const index = Math.floor(
           Math.log(bytes) / Math.log(1024)
       );
   
       const size =
           bytes / Math.pow(1024, index);
   
       return size.toFixed(2) + " " + units[index];
   }
   
   
   /* =========================================================
      VALIDATE FILE
      ========================================================= */
   
   function validateMaterialFile(file) {
   
       if (!file) {
           return {
               valid: false,
               message: "Please select a learning material."
           };
       }
   
   
       /* Check extension */
   
       const extension =
           getFileExtension(file.name);
   
       if (!ALLOWED_EXTENSIONS.includes(extension)) {
   
           return {
               valid: false,
               message:
                   "Invalid file format.\n\n" +
                   "Please upload PDF, PPT, PPTX, DOC, or DOCX."
           };
   
       }
   
   
       /* Check size */
   
       if (file.size > MAX_FILE_SIZE) {
   
           return {
               valid: false,
               message:
                   "File is too large.\n\n" +
                   "Maximum allowed size is 25 MB."
           };
   
       }
   
   
       return {
           valid: true,
           message: "File is valid."
       };
   
   }
   
   
   /* =========================================================
      DISPLAY SELECTED FILE
      ========================================================= */
   
   function displaySelectedFile(file) {
   
       const selectedFileCard =
           document.getElementById("selectedFileCard");
   
       const selectedFileName =
           document.getElementById("selectedFileName");
   
       const selectedFileSize =
           document.getElementById("selectedFileSize");
   
       const selectedFileIcon =
           document.querySelector(".selected-file-icon");
   
   
       if (!selectedFileCard || !file) {
           return;
       }
   
   
       /* File name */
   
       if (selectedFileName) {
   
           selectedFileName.textContent =
               file.name;
   
       }
   
   
       /* File size */
   
       if (selectedFileSize) {
   
           selectedFileSize.textContent =
               formatFileSize(file.size);
   
       }
   
   
       /* File type */
   
       if (selectedFileIcon) {
   
           const extension =
               getFileExtension(file.name);
   
           selectedFileIcon.textContent =
               extension.replace(".", "").toUpperCase();
   
       }
   
   
       /* Show selected file */
   
       selectedFileCard.style.display =
           "flex";
   
   }
   
   
   /* =========================================================
      HANDLE FILE SELECTION
      ========================================================= */
   
   function handleMaterialFile(file) {
   
       if (!file) {
           return;
       }
   
   
       const validation =
           validateMaterialFile(file);
   
   
       if (!validation.valid) {
   
           alert(validation.message);
   
           clearSelectedFile();
   
           return;
   
       }
   
   
       displaySelectedFile(file);
   
   }
   
   
   /* =========================================================
      FILE INPUT CHANGE
      ========================================================= */
   
   function handleFileInputChange(event) {
   
       const files = event.target.files;
   
       if (!files || files.length === 0) {
           return;
       }
   
       const file = files[0];
   
       handleMaterialFile(file);
   
   }
   
   
   /* =========================================================
      DRAG & DROP
      ========================================================= */
   
   function initializeDragAndDrop() {
   
       const dropZone =
           document.getElementById("uploadDropZone");
   
       const fileInput =
           document.getElementById("materialFile");
   
   
       if (!dropZone || !fileInput) {
           return;
       }
   
   
       /* Prevent browser default behavior */
   
       ["dragenter", "dragover", "dragleave", "drop"]
           .forEach(function (eventName) {
   
               dropZone.addEventListener(
                   eventName,
                   function (event) {
   
                       event.preventDefault();
                       event.stopPropagation();
   
                   }
               );
   
           });
   
   
       /* Highlight */
   
       ["dragenter", "dragover"]
           .forEach(function (eventName) {
   
               dropZone.addEventListener(
                   eventName,
                   function () {
   
                       dropZone.classList.add(
                           "drag-over"
                       );
   
                   }
               );
   
           });
   
   
       /* Remove highlight */
   
       ["dragleave", "drop"]
           .forEach(function (eventName) {
   
               dropZone.addEventListener(
                   eventName,
                   function () {
   
                       dropZone.classList.remove(
                           "drag-over"
                       );
   
                   }
               );
   
           });
   
   
       /* Drop */
   
       dropZone.addEventListener(
           "drop",
           function (event) {
   
               const files =
                   event.dataTransfer.files;
   
               if (!files || files.length === 0) {
                   return;
               }
   
   
               const file = files[0];
   
   
               /*
                * Put dropped file into the file input.
                * DataTransfer is supported by modern browsers.
                */
   
               try {
   
                   const dataTransfer =
                       new DataTransfer();
   
                   dataTransfer.items.add(file);
   
                   fileInput.files =
                       dataTransfer.files;
   
               } catch (error) {
   
                   console.log(
                       "Could not assign dropped file to input."
                   );
   
               }
   
   
               handleMaterialFile(file);
   
           }
       );
   
   
       /* Clicking drop zone opens file browser */
   
       dropZone.addEventListener(
           "click",
           function (event) {
   
               /*
                * Don't open browser when clicking
                * the Browse Files label itself.
                */
   
               if (
                   event.target.tagName === "LABEL" ||
                   event.target.closest("label")
               ) {
                   return;
               }
   
               fileInput.click();
   
           }
       );
   
   }
   
   
   /* =========================================================
      CLEAR SELECTED FILE
      ========================================================= */
   
   function clearSelectedFile() {
   
       const fileInput =
           document.getElementById("materialFile");
   
       const selectedFileCard =
           document.getElementById("selectedFileCard");
   
   
       if (fileInput) {
   
           fileInput.value = "";
   
       }
   
   
       if (selectedFileCard) {
   
           selectedFileCard.style.display =
               "none";
   
       }
   
   }
   
   
   /* =========================================================
      REMOVE FILE BUTTON
      ========================================================= */
   
   function initializeRemoveFileButton() {
   
       const removeButton =
           document.getElementById("removeFileBtn");
   
   
       if (!removeButton) {
           return;
       }
   
   
       removeButton.addEventListener(
           "click",
           function () {
   
               clearSelectedFile();
   
           }
       );
   
   }
   
   
   /* =========================================================
      CLEAR UPLOAD FORM
      ========================================================= */
   
   function clearUploadForm() {
   
       const fileInput =
           document.getElementById("materialFile");
   
       const titleInput =
           document.getElementById("materialTitle");
   
       const competency =
           document.getElementById("materialCompetency");
   
       const topic =
           document.getElementById("materialTopic");
   
       const description =
           document.getElementById("materialDescription");
   
       const uploadStatus =
           document.getElementById("uploadStatus");
   
   
       /* Clear file */
   
       if (fileInput) {
   
           fileInput.value = "";
   
       }
   
   
       /* Clear selected file */
   
       const selectedFileCard =
           document.getElementById("selectedFileCard");
   
       if (selectedFileCard) {
   
           selectedFileCard.style.display =
               "none";
   
       }
   
   
       /* Clear form */
   
       if (titleInput) {
           titleInput.value = "";
       }
   
       if (competency) {
           competency.value = "";
       }
   
       if (topic) {
           topic.value = "";
       }
   
       if (description) {
           description.value = "";
       }
   
   
       /* Hide status */
   
       if (uploadStatus) {
   
           uploadStatus.style.display =
               "none";
   
       }
   
   }
   
   
   /* =========================================================
      SHOW UPLOAD STATUS
      ========================================================= */
   
   function showUploadStatus(title, message) {
   
       const uploadStatus =
           document.getElementById("uploadStatus");
   
       const statusTitle =
           document.getElementById("uploadStatusTitle");
   
       const statusText =
           document.getElementById("uploadStatusText");
   
   
       if (!uploadStatus) {
           return;
       }
   
   
       if (statusTitle) {
   
           statusTitle.textContent =
               title;
   
       }
   
   
       if (statusText) {
   
           statusText.textContent =
               message;
   
       }
   
   
       uploadStatus.style.display =
           "flex";
   
   }
   
   
   /* =========================================================
      UPLOAD MATERIAL
      ========================================================= */
   
   function uploadMaterial() {
   
       const fileInput =
           document.getElementById("materialFile");
   
       const titleInput =
           document.getElementById("materialTitle");
   
       const competency =
           document.getElementById("materialCompetency");
   
       const topic =
           document.getElementById("materialTopic");
   
       const description =
           document.getElementById("materialDescription");
   
   
       /* Check file */
   
       if (
           !fileInput ||
           !fileInput.files ||
           fileInput.files.length === 0
       ) {
   
           alert(
               "Please select a learning material first."
           );
   
           return;
   
       }
   
   
       const file =
           fileInput.files[0];
   
   
       /* Validate file */
   
       const validation =
           validateMaterialFile(file);
   
   
       if (!validation.valid) {
   
           alert(validation.message);
   
           return;
   
       }
   
   
       /* Check title */
   
       if (
           !titleInput ||
           titleInput.value.trim() === ""
       ) {
   
           alert(
               "Please enter the material title."
           );
   
           if (titleInput) {
               titleInput.focus();
           }
   
           return;
   
       }
   
   
       /* Check competency */
   
       if (
           !competency ||
           competency.value === ""
       ) {
   
           alert(
               "Please select a competency."
           );
   
           if (competency) {
               competency.focus();
           }
   
           return;
   
       }
   
   
       /* Check topic */
   
       if (
           !topic ||
           topic.value === ""
       ) {
   
           alert(
               "Please select a topic."
           );
   
           if (topic) {
               topic.focus();
           }
   
           return;
   
       }
   
   
       /* =====================================================
          DEMO PROCESSING
          ===================================================== */
   
       showUploadStatus(
           "Processing material...",
           "Preparing the document for AI processing."
       );
   
   
       const uploadButton =
           document.getElementById("uploadMaterialBtn");
   
       if (uploadButton) {
   
           uploadButton.disabled = true;
   
           uploadButton.style.opacity =
               "0.6";
   
           uploadButton.textContent =
               "Processing...";
   
       }
   
   
       /*
        * DEMO ONLY
        *
        * Later this section will be replaced with
        * a fetch() request to the Flask backend.
        */
   
       setTimeout(function () {
   
           showUploadStatus(
               "Material uploaded successfully",
               "The document is ready for backend processing."
           );
   
   
           if (uploadButton) {
   
               uploadButton.disabled = false;
   
               uploadButton.style.opacity =
                   "1";
   
               uploadButton.textContent =
                   "Upload Material";
   
           }
   
   
       }, 2000);
   
   }
   
   
   /* =========================================================
      UPLOAD BUTTON
      ========================================================= */
   
   function initializeUploadButton() {
   
       const uploadButton =
           document.getElementById("uploadMaterialBtn");
   
   
       if (!uploadButton) {
           return;
       }
   
   
       uploadButton.addEventListener(
           "click",
           uploadMaterial
       );
   
   }
   
   
   /* =========================================================
      CLEAR BUTTON
      ========================================================= */
   
   function initializeClearButton() {
   
       const clearButton =
           document.getElementById("clearUploadBtn");
   
   
       if (!clearButton) {
           return;
       }
   
   
       clearButton.addEventListener(
           "click",
           clearUploadForm
       );
   
   }
   
   
   /* =========================================================
      APPROVE AI QUESTION
      ========================================================= */
   
   function approveQuestion(button) {
   
       const row =
           button.closest("tr");
   
   
       /*
        * New dashboard uses .quiz-question
        * instead of table rows.
        */
   
       if (!row) {
   
           const questionCard =
               button.closest(".quiz-question");
   
           if (!questionCard) {
               return;
           }
   
   
           button.textContent =
               "Approved";
   
           button.disabled = true;
   
           button.style.opacity =
               "0.6";
   
   
           const flagButton =
               questionCard.querySelector(
                   ".flag-btn"
               );
   
           if (flagButton) {
   
               flagButton.disabled = true;
   
               flagButton.style.opacity =
                   "0.5";
   
           }
   
   
           questionCard.style.opacity =
               "0.75";
   
           return;
   
       }
   
   
       /* Old table support */
   
       const question =
           row.querySelector(".question-cell");
   
       const flagButton =
           row.querySelector(".flag-btn");
   
   
       button.textContent =
           "Approved";
   
       button.disabled = true;
   
       button.style.opacity =
           "0.6";
   
   
       if (flagButton) {
   
           flagButton.disabled = true;
   
           flagButton.style.opacity =
               "0.5";
   
       }
   
   
       if (question) {
   
           question.style.opacity =
               "0.65";
   
       }
   
   }
   
   
   /* =========================================================
      FLAG AI QUESTION
      ========================================================= */
   
   function flagQuestion(button) {
   
       const row =
           button.closest("tr");
   
   
       /*
        * New dashboard support
        */
   
       if (!row) {
   
           const questionCard =
               button.closest(".quiz-question");
   
           if (!questionCard) {
               return;
           }
   
   
           button.textContent =
               "Flagged";
   
           button.disabled = true;
   
           button.style.opacity =
               "0.6";
   
   
           const approveButton =
               questionCard.querySelector(
                   ".approve-btn"
               );
   
           if (approveButton) {
   
               approveButton.disabled = true;
   
               approveButton.style.opacity =
                   "0.5";
   
           }
   
   
           const questionFooter =
               questionCard.querySelector(
                   ".question-footer"
               );
   
           if (questionFooter) {
   
               const topic =
                   questionFooter.querySelector(
                       "span"
                   );
   
               if (topic) {
   
                   topic.textContent =
                       "⚠ Flagged";
   
                   topic.style.color =
                       "#b91c1c";
   
               }
   
           }
   
           return;
   
       }
   
   
       /* Old table support */
   
       const validation =
           row.querySelector(".validation");
   
   
       button.textContent =
           "Flagged";
   
       button.disabled = true;
   
       button.style.opacity =
           "0.6";
   
   
       if (validation) {
   
           validation.textContent =
               "⚠ Flagged";
   
           validation.style.color =
               "#b91c1c";
   
       }
   
   }
   
   
   /* =========================================================
      SMOOTH SCROLL
      ========================================================= */
   
   function scrollToSection(sectionId) {
   
       const section =
           document.getElementById(sectionId);
   
   
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
   
   document.addEventListener(
       "DOMContentLoaded",
       function () {
   
           const fileInput =
               document.getElementById(
                   "materialFile"
               );
   
   
           /* File selection */
   
           if (fileInput) {
   
               fileInput.addEventListener(
                   "change",
                   handleFileInputChange
               );
   
           }
   
   
           /* Drag and drop */
   
           initializeDragAndDrop();
   
   
           /* Remove selected file */
   
           initializeRemoveFileButton();
   
   
           /* Upload button */
   
           initializeUploadButton();
   
   
           /* Clear button */
   
           initializeClearButton();
   
       }
   );