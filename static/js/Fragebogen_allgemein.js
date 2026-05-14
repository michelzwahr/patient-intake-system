page1()
function page1(){
    document.getElementById("personal_info").style.display = "block";
    document.getElementById("regelanamnese").style.display = "none";
}

function page2(){
    document.getElementById("personal_info").style.display = "none";
    document.getElementById("regelanamnese").style.display = "block";
    document.getElementById("contraception").style.display = "none";
}

function page3(){
    document.getElementById("contraception").style.display = "block";
    document.getElementById("regelanamnese").style.display = "none";
    document.getElementById("acute_symptoms").style.display = "none";
}

function page4(){
    document.getElementById("contraception").style.display = "none";
    document.getElementById("acute_symptoms").style.display = "block";
}

function period_regulary(){
    const selected_radio = document.querySelector('input[name="period_regulary"]:checked').value;
    const period_regulary_div = document.getElementById("period_regulary_div");

    if (selected_radio == "nein"){
        period_regulary_div.style.display = "block"
    }
    else{
        period_regulary_div.style.display = "none"
    }   
}
function toggleAcuteSymptoms(){
    const selectedRadio = document.querySelector('input[name="acute_symptoms"]:checked');
    const acuteSymptomsDiv = document.getElementById("acute_symptoms_div");

    if (!selectedRadio || !acuteSymptomsDiv) {
        return;
    }

    if (selectedRadio.value === "ja"){
        acuteSymptomsDiv.style.display = "block";
    }
    else{
        acuteSymptomsDiv.style.display = "none";
    }
}


function addRow() {

    const container = document.getElementById("contraception-list");

    const row = document.createElement("div");
    row.classList.add("contraception-row");

    row.innerHTML = `
        <input type="text" placeholder="Methode">

        <input type="number"
                   placeholder="Von"
                   min="1900"
                   max="2100">

            <input type="number"
                   placeholder="Bis"
                   min="1900"
                   max="2100">

        <button type="button" onclick="removeRow(this)">
            ✕
        </button>
    `;

    container.appendChild(row);
}

function removeRow(button) {
    button.parentElement.remove();
}
