document.addEventListener("DOMContentLoaded", function () {
  const submitBtn = document.getElementById("submitBtn");

  submitBtn.addEventListener("click", function () {
    const teamName = document.getElementById("nameinput").value.trim();
    if (!teamName) {
      alert("Please enter team name!");
      return;
    }

    fetch("http://localhost:8000/team_info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: teamName }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert("Error: " + data.error);
          return;
        }

        const info = data.team_info;
        const container = document.getElementById("pdf");
        container.innerHTML = ""; // Очищаємо попередній результат

        for (const [key, value] of Object.entries(info)) {
          const block = document.createElement("div");
          block.className = "section";
          block.style.marginBottom = "30px";
          block.style.padding = "10px";
          block.style.borderBottom = "1px solid #ccc";
          block.style.textAlign = "center"; // Центруємо все в блоці

          const title = document.createElement("h3");
          title.textContent = key;
          title.style.textAlign = "center"; // Центруємо заголовок
          block.appendChild(title);

          if (typeof value === "string") {
            if (value.startsWith("<")) {
              const div = document.createElement("div");
              div.innerHTML = value;
              div.style.display = "inline-block"; // Щоб таблиця була по центру
              block.appendChild(div);
            } else if (value.startsWith("http")) {
              const link = document.createElement("a");
              link.href = value;
              link.target = "_blank";
              link.textContent = value;
              link.style.display = "block";
              link.style.margin = "10px auto";
              block.appendChild(link);
            } else {
              const text = document.createElement("p");
              text.textContent = value;
              text.style.textAlign = "center";
              block.appendChild(text);
            }
          } else if (Array.isArray(value)) {
            if (value.length && value[0].startsWith("http")) {
              value.forEach((url) => {
                if (url.includes("youtube")) {
                  const videoId = url.split("v=")[1]?.split("&")[0];
                  if (videoId) {
                    const iframe = document.createElement("iframe");
                    iframe.width = "300";
                    iframe.height = "170";
                    iframe.src = `https://www.youtube.com/embed/${videoId}`;
                    iframe.frameBorder = "0";
                    iframe.allow =
                      "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
                    iframe.allowFullscreen = true;
                    iframe.style.margin = "10px auto";
                    iframe.style.display = "block";
                    block.appendChild(iframe);
                  }
                } else {
                  const img = document.createElement("img");
                  img.src = url;
                  img.alt = "image";
                  img.style.maxWidth = "200px";
                  img.style.margin = "10px";
                  block.appendChild(img);
                }
              });
            } else {
              const ul = document.createElement("ul");
              ul.style.display = "inline-block";
              ul.style.textAlign = "left";
              value.forEach((v) => {
                const li = document.createElement("li");
                li.textContent = v;
                ul.appendChild(li);
              });
              block.appendChild(ul);
            }
          } else if (typeof value === "object") {
            for (const [name, image] of Object.entries(value)) {
              const player = document.createElement("p");
              player.innerHTML = `<strong>${name}</strong>`;
              block.appendChild(player);
              const img = document.createElement("img");
              img.src = image;
              img.alt = name;
              img.style.maxWidth = "200px";
              img.style.margin = "10px";
              block.appendChild(img);
            }
          }

          container.appendChild(block);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Something went wrong");
      });
  });
});
