page1()
function page1(){
    document.getElementById("personal_info").style.display = "block";
    document.getElementById("regelanamnese").style.display = "none";
    
}

function page2(){
    document.getElementById("personal_info").style.display = "none";
    document.getElementById("regelanamnese").style.display = "block";
    
}

function period_regulary(){
    const selected_radio = document.querySelector('input[name="period_regulary"]:checked').value;
    const allergy_div = document.getElementById("period_regulary_div");

    if (selected_radio == "nein"){
        allergy_div.style = "display: block;"
    }
    else{
        allergy_div.style = "display: none;"
    }
    
}