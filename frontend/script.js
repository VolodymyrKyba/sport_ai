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
          block.style.marginBottom = "30px"; // відступ між блоками
          block.style.padding = "10px";
          block.style.borderBottom = "1px solid #ccc";

          const title = document.createElement("h3");
          title.textContent = key;
          block.appendChild(title);

          if (typeof value === "string") {
            if (value.startsWith("<")) {
              // HTML таблиця
              const div = document.createElement("div");
              div.innerHTML = value;
              block.appendChild(div);
            } else if (value.startsWith("http")) {
              const link = document.createElement("a");
              link.href = value;
              link.target = "_blank";
              link.textContent = value;
              block.appendChild(link);
            } else {
              const text = document.createElement("p");
              text.textContent = value;
              block.appendChild(text);
            }
          } else if (Array.isArray(value)) {
            if (value.length && value[0].startsWith("http")) {
              value.forEach((url) => {
                if (url.includes("youtube")) {
                  const iframe = document.createElement("iframe");
                  iframe.width = "300";
                  iframe.height = "170";
                  iframe.src = url.replace("watch?v=", "embed/");
                  iframe.frameBorder = "0";
                  iframe.allowFullscreen = true;
                  block.appendChild(iframe);
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
