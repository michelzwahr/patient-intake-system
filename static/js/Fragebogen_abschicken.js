function getValue(id) {
    const element = document.getElementById(id);
    return element ? element.value : "";
}

function getCheckedValue(name) {
    const checked = document.querySelector(`input[name="${name}"]:checked`);
    return checked ? checked.value : "";
}

function collectContraceptionRows() {
    return Array.from(document.querySelectorAll("#contraception-list .contraception-row"))
        .map((row) => {
            const inputs = row.querySelectorAll("input");

            return {
                method: inputs[0] ? inputs[0].value : "",
                from: inputs[1] ? inputs[1].value : "",
                to: inputs[2] ? inputs[2].value : ""
            };
        })
        .filter((entry) => entry.method || entry.from || entry.to);
}

function collectMedicationRows() {
    return Array.from(document.querySelectorAll("#medication-list .medication-row"))
        .map((row) => {
            const inputs = row.querySelectorAll("input");

            return {
                name: inputs[0] ? inputs[0].value : "",
                dose: inputs[1] ? inputs[1].value : "",
                since: inputs[2] ? inputs[2].value : ""
            };
        })
        .filter((entry) => entry.name || entry.dose || entry.since);
}

function collectQuestionnaireData() {
    return {
        fname: getValue("fname"),
        name: getValue("name"),
        date: getValue("date"),
        phone: getValue("phone"),
        adress: getValue("adress"),
        hausarzt: getValue("hausarzt"),
        other_doctors: getValue("other_doctors"),
        first_period: getValue("first_period"),
        last_period: getValue("last_period"),
        period_regulary: getCheckedValue("period_regulary"),
        period_regulary_details: getValue("period_regulary_details"),
        contraception: collectContraceptionRows(),
        acute_symptoms: getCheckedValue("acute_symptoms"),
        acute_symptoms_details: getValue("acute_symptoms_details"),
        disease: getCheckedValue("disease"),
        disease_details: getValue("disease_details"),
        gen_op: getCheckedValue("gen_op"),
        gen_op_details: getValue("gen_op_details"),
        gyn_op: getCheckedValue("gyn_op"),
        gyn_op_details: getValue("gyn_op_details"),
        births: getCheckedValue("births"),
        births_nb: getValue("births_nb"),
        births_time: getValue("births_time"),
        births_complications: getValue("births_complications"),
        miscarriage: getCheckedValue("miscarriage"),
        miscarriage_details: getValue("miscarriage_details"),
        child_desire: getCheckedValue("child_desire"),
        child_desire_details: getValue("child_desire_details"),
        pregnancy: getCheckedValue("pregnancy"),
        pregnancy_details: getValue("pregnancy_details"),
        last_period_pregnancy: getValue("last_period_pregnancy"),
        medications: collectMedicationRows(),
        allergy: getCheckedValue("allergy"),
        allergy_details: getValue("allergy_details"),
        nic: getCheckedValue("nic"),
        cannabis: getCheckedValue("cannabis"),
        alc: getCheckedValue("alc"),
        other_drugs: getCheckedValue("other_drugs"),
        personal_matter: getCheckedValue("personal_matter"),
        personal_matter_details: getValue("personal_matter_details")
    };
}

async function submitQuestionnaire() {
    const data = collectQuestionnaireData();

    try {
        const response = await fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`POST /submit failed with status ${response.status}`);
        }

        await response.json();
        window.location.href = "/success";
    }
    catch (error) {
        console.error("Fehler beim Senden des Fragebogens:", error);
        window.alert("Beim Abschicken des Fragebogens ist ein Fehler aufgetreten.");
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById("submit-questionnaire");

    if (!submitButton) {
        return;
    }

    submitButton.addEventListener("click", submitQuestionnaire);
});
