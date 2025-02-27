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
      body: JSON.stringify({ name: userName }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("response").innerText = data.message;

        const logoUrl = data.logo_url;

        if (logoUrl) {
          const logoElement = document.getElementById("logoImage");
          logoElement.src = logoUrl;
          logoElement.alt = `${userName} Logo`;
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
