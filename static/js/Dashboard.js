const patientSelect = document.getElementById("patient-select");
const formsSelect = document.getElementById("forms");
const patientInfo = document.getElementById("patient-info");

const patientTemplate = document.getElementById("patient-template");
const medicationTemplate = document.getElementById("medication-template");
const contraceptionTemplate = document.getElementById("contraception-template");
const selectionTemplate = document.getElementById("selection-template");

let currentFormsData = [];

function logout(){
    window.location.href = `/logout`;
}

function download_file(){
    const selectedForm = formsSelect.value;
    const dataSet = currentFormsData[selectedForm];
    path = dataSet.filepath;
    //console.log(path);
    window.location.href = `/download/${path}`;
}

async function search_patient(){
    const patient_str = document.getElementById("patient-name").value;
    const response = await fetch(`/search/${patient_str}`);
    const patients = await response.json();

    patientSelect.innerHTML = "<option>Bitte auswählen</option>";

    patients.forEach((result) => {
        const newOption = document.createElement("option");
        newOption.value = result.id;
        newOption.textContent = `${result.fname} ${result.name}`;
        patientSelect.appendChild(newOption);
    })
}

function setTextContent(container, selector, value) {
    const element = container.querySelector(selector);

    if (element) {
        element.textContent = value ?? "";
    }
}


function formatConditionalValue(flag, details, yesText = "Ja", noText = "Nein") {
    if (flag === "ja") {
        return details || yesText;
    }

    return noText;
}

function renderPatientForm(dataSet) {
    patientInfo.style.display = "block";
    patientInfo.innerHTML = "";

    if (!dataSet) {
        return;
    }

    const clone = patientTemplate.content.cloneNode(true);

    setTextContent(clone, ".name", `${dataSet.fname} ${dataSet.name}`);
    setTextContent(clone, ".date", dataSet.date);
    setTextContent(clone, ".phone", dataSet.phone);
    setTextContent(clone, ".adress", dataSet.adress);
    setTextContent(clone, ".first_period", dataSet.first_period);
    setTextContent(clone, ".last_period", dataSet.last_period);
    setTextContent(
        clone,
        ".period",
        dataSet.period_regulary === "ja" ? "regelmaessig" : dataSet.period_regulary_details
    );
    setTextContent(
        clone,
        ".acute_symptoms",
        formatConditionalValue(dataSet.acute_symptoms, dataSet.acute_symptoms_details)
    );
    setTextContent(
        clone,
        ".disease",
        formatConditionalValue(dataSet.disease, dataSet.disease_details)
    );
    setTextContent(
        clone,
        ".gen_op",
        formatConditionalValue(dataSet.gen_op, dataSet.gen_op_details)
    );
    setTextContent(
        clone,
        ".gyn_op",
        formatConditionalValue(dataSet.gyn_op, dataSet.gyn_op_details)
    );
    if (dataSet.births == "ja"){
        setTextContent(
            clone,
            ".births_nb",
            dataSet.births_nb || "Keine Angabe"
        );
        setTextContent(
            clone,
            ".births_time",
            dataSet.births_time || "Keine Angabe"
        );
        setTextContent(
            clone,
            ".births_complications",
            dataSet.births_complications || "Nein"
        );
    }
    else{
        clone.querySelectorAll(".births").forEach((element) => {
            element.style.display = "none";
        })
        console.log(clone.querySelectorAll(".births"));
        setTextContent(clone, ".births_nb", "0");
    }
    setTextContent(clone, ".miscarriage", dataSet.miscarriage_details || "Nein");
    setTextContent(
        clone,
        ".child_desire",
        formatConditionalValue(dataSet.child_desire, "seit " + dataSet.child_desire_details)
    );
    setTextContent(
        clone,
        ".pregnancy",
        formatConditionalValue(dataSet.pregnancy, dataSet.pregnancy_details)
    );
    setTextContent(
        clone,
        ".allergies",
        formatConditionalValue(dataSet.allergy, dataSet.allergy_details)
    );
    setTextContent(clone, ".alc", dataSet.alc);
    setTextContent(clone, ".nic", dataSet.nic);
    setTextContent(clone, ".cannabis", dataSet.cannabis);
    setTextContent(clone, ".other_drugs", dataSet.other_drugs);
    setTextContent(
        clone,
        ".personal_matter",
        formatConditionalValue(dataSet.personal_matter, dataSet.personal_matter_details)
    );

    const contraceptionList = clone.querySelector(".contraception-list");
    (dataSet.contraception || []).forEach((method) => {
        const contraceptionClone = contraceptionTemplate.content.cloneNode(true);

        setTextContent(contraceptionClone, ".con_method", method.method);
        setTextContent(contraceptionClone, ".con_from", method.from);
        setTextContent(contraceptionClone, ".con_to", method.to);

        contraceptionList.appendChild(contraceptionClone);
    });

    const medicationList = clone.querySelector(".medication-list");
    (dataSet.medications || []).forEach((medication) => {
        const medicationClone = medicationTemplate.content.cloneNode(true);

        setTextContent(medicationClone, ".med_name", medication.name);
        setTextContent(medicationClone, ".med_dose", medication.dose);
        setTextContent(medicationClone, ".med_since", medication.since);

        medicationList.appendChild(medicationClone);
    });

    patientInfo.appendChild(clone);
}

patientSelect.addEventListener("change", async () => {
    const patientId = patientSelect.value;

    currentFormsData = [];
    formsSelect.innerHTML = "<option value=''>Bitte auswählen</option>";
    patientInfo.innerHTML = "";

    if (!patientId) {
        return;
    }

    const response = await fetch(`/patient/${patientId}`);
    currentFormsData = await response.json();

    currentFormsData.forEach((dataSet, index) => {
        const optionClone = selectionTemplate.content.cloneNode(true);
        const option = optionClone.querySelector("option");

        option.value = index;
        option.textContent = dataSet.filename;
        

        formsSelect.appendChild(optionClone);
    });
});

formsSelect.addEventListener("change", () => {
    const selectedForm = formsSelect.value;
    const dataSet = currentFormsData[selectedForm];

    if (dataset){
        switch (dataSet.type){
            case "Fragebogen_allgemein":
                renderPatientForm(dataSet);
        }
    }
});

