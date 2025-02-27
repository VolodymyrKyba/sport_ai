const scrollButton = document.getElementById("scrollButton");

// Обробник події для кнопки
scrollButton.addEventListener("click", function () {
  // Імітація скролу вниз
  window.scrollBy({
    top: 500, // Кількість пікселів для прокручування вниз
    left: 0,
    behavior: "smooth", // Плавна анімація прокручування
  });
});
