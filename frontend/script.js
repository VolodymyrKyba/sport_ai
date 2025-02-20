document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("submitBtn").addEventListener("click", function () {
    let userName = document.getElementById("nameinput").value;

    if (!userName) {
      alert("Please enter your name!");
      return;
    }

    fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: userName }), // Send input as JSON
    })
      .then((response) => response.json()) // Convert response to JSON
      .then((data) => {
        document.getElementById("response").innerText = data.message; // Display response
      })
      .catch((error) => console.error("Error:", error));
  });
});
