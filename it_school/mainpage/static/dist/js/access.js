// Этот скрипт может использоваться для анимированных эффектов на странице

// Пример анимации - мигание заголовка h1
function blinkHeader() {
    var header = document.querySelector('h1');
    setInterval(function() {
        header.classList.toggle('blink');
    }, 500);
}

blinkHeader();
