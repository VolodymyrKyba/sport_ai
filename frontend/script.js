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

        const banner_Url = data.banner_url;

        if (banner_Url) {
          const banner_Element = document.getElementById("bannerImage");
          banner_Element.src = banner_Url;
        }
        const formUrl = data.unifrom_url;

        if (formUrl) {
          const formElement = document.getElementById("uniform");
          formElement.src = formUrl;
        }
        const logo_Url = data.logo;

        if (logo_Url) {
          const logoElement = document.getElementById("logoImage");
          logoElement.src = logo_Url;
        }

        const nickName = data.nick_name;

        if (nickName) {
          document.getElementById("nickNameDisplay").innerText = nickName;
        }

        const l_5_events = data.last_5_events;

        if (l_5_events) {
          document.getElementById("l_5_events").innerHTML = l_5_events;
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
