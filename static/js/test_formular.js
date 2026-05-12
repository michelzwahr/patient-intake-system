document.getElementById("testform").addEventListener("submit", function(event) {
    event.preventDefault(); // verhindert Seitenreload

    const fname = document.getElementById("fname").value;
    const name = document.getElementById("name").value;

    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            fname: fname,
            name: name
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        window.location.href = "/success";
    });

});
