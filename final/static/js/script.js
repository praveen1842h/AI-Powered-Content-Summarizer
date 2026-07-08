// ==========================================
// SUMMARAI PRO
// MAIN JAVASCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", function () {


    const inputText = document.getElementById("inputText");

    const wordCount = document.getElementById("wordCount");

    const characterCount = document.getElementById("characterCount");

    const readingTime = document.getElementById("readingTime");

    const clearBtn = document.getElementById("clearBtn");

    const copyBtn = document.getElementById("copyBtn");

    const summaryResult = document.getElementById("summaryResult");



    // ======================================
    // TEXT STATISTICS
    // ======================================

    function updateStats() {


        if (!inputText) {

            return;

        }


        let text = inputText.value.trim();


        let words = 0;


        if (text.length > 0) {

            words = text.split(/\s+/).length;

        }


        let characters = text.length;


        let minutes = Math.ceil(words / 200);


        if (minutes < 1) {

            minutes = 0;

        }



        if (wordCount) {

            wordCount.innerText = words;

        }


        if (characterCount) {

            characterCount.innerText = characters;

        }


        if (readingTime) {

            readingTime.innerText = minutes;

        }

    }



    if (inputText) {


        inputText.addEventListener(
            "input",
            updateStats
        );


        updateStats();

    }



    // ======================================
    // CLEAR TEXT
    // ======================================

    if (clearBtn) {


        clearBtn.addEventListener(
            "click",
            function () {


                if (inputText) {

                    inputText.value = "";

                }


                updateStats();


            }
        );


    }



    // ======================================
    // COPY SUMMARY
    // ======================================

    if (copyBtn) {


        copyBtn.addEventListener(
            "click",
            function () {


                if (!summaryResult) {

                    return;

                }


                const text =
                    summaryResult.innerText;



                navigator.clipboard.writeText(text)
                .then(function () {


                    copyBtn.innerHTML =
                    '<i class="fa-solid fa-check"></i> Copied';



                    setTimeout(function () {


                        copyBtn.innerHTML =
                        '<i class="fa-solid fa-copy"></i> Copy';



                    },2000);



                });



            }
        );


    }



    // ======================================
    // FORM LOADING
    // ======================================

    const summaryForm =
        document.getElementById("summaryForm");


    if (summaryForm) {


        summaryForm.addEventListener(
            "submit",
            function () {


                const button =
                    summaryForm.querySelector(
                        "button[type='submit']"
                    );


                if (button) {


                    button.innerHTML =
                    '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';


                    button.disabled = true;


                }


            }
        );


    }



});