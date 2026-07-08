// ==========================================
// SUMMARAI PRO
// SPEECH TO TEXT
// ==========================================

document.addEventListener("DOMContentLoaded", () => {


    const voiceBtn = document.getElementById(
        "voiceBtn"
    );


    const inputText = document.getElementById(
        "inputText"
    );


    if (!voiceBtn || !inputText) {

        return;

    }


    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {


        voiceBtn.disabled = true;


        voiceBtn.innerHTML =
            '<i class="fa-solid fa-microphone-slash"></i> Not Supported';


        return;


    }


    const recognition =
        new SpeechRecognition();


    recognition.continuous = false;


    recognition.interimResults = true;


    recognition.lang = "en-US";



    voiceBtn.addEventListener(
        "click",
        () => {


            recognition.start();


            voiceBtn.innerHTML =
                '<i class="fa-solid fa-circle-stop"></i> Listening';


        }
    );



    recognition.onresult = (event) => {


        let speechText = "";


        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {


            speechText +=
                event.results[i][0].transcript;


        }


        inputText.value =
            speechText;



        inputText.dispatchEvent(
            new Event("input")
        );


    };



    recognition.onend = () => {


        voiceBtn.innerHTML =
            '<i class="fa-solid fa-microphone"></i> Voice';


    };



    recognition.onerror = () => {


        voiceBtn.innerHTML =
            '<i class="fa-solid fa-microphone"></i> Voice';


        alert(
            "Voice recognition failed. Please try again."
        );


    };


});