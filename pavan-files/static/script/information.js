document
  .getElementById("info-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    fetch("/introduce_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const aiResponseDiv = document.getElementById("ai-response");
        const responseText = document.getElementById("response-text");

        if (data.error) {
          responseText.textContent = data.error;
        } else {
          responseText.innerHTML = data.response;
        }

        aiResponseDiv.style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
