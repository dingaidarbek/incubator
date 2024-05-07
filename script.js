document.addEventListener("DOMContentLoaded", function () {
    fetch('users.json')
        .then(response => response.json())
        .then(data => {
            const dataDisplay = document.getElementById("dataDisplay");

            
            // Create HTML elements to display the JSON data
            const nameElement = document.createElement("p");
            nameElement.textContent = "Name: " + data.login;


            const ageElement = document.createElement("p");
            ageElement.textContent = "Age: " + data.password;



            // Append the elements to the "dataDisplay" div
            dataDisplay.appendChild(nameElement);
            dataDisplay.appendChild(ageElement);
            dataDisplay.appendChild(cityElement);
        })
        .catch(error => console.error("Error fetching JSON data:", error));
});