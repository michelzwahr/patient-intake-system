document.getElementById("testform").addEventListener("submit", function(event) {
    event.preventDefault(); // verhindert Seitenreload

    const fname = document.getElementById("fname").value;
    const name = document.getElementById("name").value;
    
    const selected_radio = document.querySelector('input[name="allergy"]:checked').value;
    const allergy_details = document.getElementById("allergy_details");



    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            fname: fname,
            name: name,
            allergies: selected_radio,
            allergy_details: allergy_details.value
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        window.location.href = "/success";
    });

});


function allergy_check(){
    const selected_radio = document.querySelector('input[name="allergy"]:checked').value;
    const allergy_div = document.getElementById("allergy_div");

    if (selected_radio == "ja"){
        allergy_div.style = "display: block;"
    }
    else{
        allergy_div.style = "display: none;"
    }
    
}
