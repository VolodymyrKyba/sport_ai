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
        document.getElementById("response").innerHTML = data.message;

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

        const teamYear = data.team_year;

        if (teamYear) {
          document.getElementById("year").innerText = teamYear;
        }

        const teamWeb = data.team_website;

        if (teamWeb) {
          const weblink = document.getElementById("website");
          weblink.href = teamWeb.startsWith("http")
            ? teamWeb
            : "https://" + teamWeb;
          weblink.style.display = "block";
          weblink.textContent = "Website";
        }

        const teamFace = data.team_facebook;

        if (teamFace) {
          const facelink = document.getElementById("facebook");
          facelink.href = teamFace.startsWith("http")
            ? teamFace
            : "https://" + teamFace;
          facelink.style.display = "block";
          facelink.textContent = "Facebook";
        }

        const teamTwit = data.team_twitter;

        if (teamTwit) {
          const twitterLink = document.getElementById("twitter");
          twitterLink.href = teamTwit.startsWith("http")
            ? teamTwit
            : "https://" + teamTwit;
          twitterLink.style.display = "block";
          twitterLink.textContent = "Twitter";
        }

        const teamInst = data.team_inst;

        if (teamInst) {
          const instlink = document.getElementById("instagram");
          instlink.href = teamInst.startsWith("http")
            ? teamInst
            : "https://" + teamInst;
          instlink.style.display = "block";
          instlink.textContent = "Instagram";
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
