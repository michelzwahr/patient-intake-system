pages = ["start_page", "personal_info", "regelanamnese", "contraception", "symptoms_disease", "ops", "birth", "medications", "drugs"]
current_page = 0;

function next(){
    document.getElementById(pages[current_page]).style.display = "none";
    document.getElementById(pages[current_page + 1]).style.display = "block";
    current_page++;
}
function back(){
    document.getElementById(pages[current_page]).style.display = "none";
    document.getElementById(pages[current_page - 1]).style.display = "block";
    current_page--;
}

function toggleSection(radioName, targetId, triggerValue = "ja") {

    const selectedRadio = document.querySelector(`input[name="${radioName}"]:checked`);

    const target = document.getElementById(targetId);

    if (!selectedRadio || !target) {
        return;
    }

    if (selectedRadio.value === triggerValue) {
        target.style.display = "block";
    }
    else {
        target.style.display = "none";
    }
}


function addContraception() {

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
function addMedication() {

    const container = document.getElementById("medication-list");

    const row = document.createElement("div");
    row.classList.add("medication-row");

    row.innerHTML = `
        <input type="text" placeholder="Name">

        <input type="text"
            placeholder="Dosis">

        <input type="number"
            placeholder="Seit">

        <button type="button" onclick="removeRow(this)">
            ✕
        </button>
    `;

    container.appendChild(row);
}

function removeRow(button) {
    button.parentElement.remove();
}
