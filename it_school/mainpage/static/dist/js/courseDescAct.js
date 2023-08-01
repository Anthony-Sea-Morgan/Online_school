function createDetailPiece() {
  const piece = document.createElement('div');
  piece.classList.add('course-detail-texture');
  return piece;
}

const detailContainer = document.getElementById('puzzleContainer');
const containerWidth = detailContainer.offsetWidth;
const containerHeight = detailContainer.offsetHeight;
for (let i = 0; i < 10; i++) {
  const piece = createDetailPiece();
  detailContainer.appendChild(piece);
}

const detailPieces = document.querySelectorAll('.course-detail-texture');


function movePiecesSlowly() {
  const centerX = containerWidth * 0.8;
  const centerY = containerHeight * 0.7;

  detailPieces.forEach(piece => {
    // Генерируем случайный радиус для частицы
    const randomRadius = Math.random() * 200 + 750;
    // Генерируем случайный угол от 0 до 2 * PI (360 градусов)
    const randomAngle = Math.random() * 2 * Math.PI;

    let angle = randomAngle;

    function animatePiece() {
      // Вычисляем новые координаты частицы на основе полярных координат
      const x = centerX + randomRadius * Math.cos(angle);
      const y = centerY + randomRadius * Math.sin(angle);

      // Увеличиваем угол, чтобы частица вращалась вокруг "папки"
      angle += Math.PI / 180; // Здесь можно настроить скорость вращения частицы

      // Устанавливаем новую позицию
      piece.style.transform = `translate(${x}px, ${y}px)`;

      // Запускаем анимацию
      requestAnimationFrame(animatePiece);
    }

    animatePiece();
  });
}

movePiecesSlowly();







function scrollToAnchor(anchorId) {
  const anchor = document.getElementById(anchorId);
  if (anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
}
if (makeLayer('reg-blank-payconf', 'flex', 'confirm_payment', 'wrapper-blank-close-btn-payconf') == 0){
document.getElementById('LOGIN-redirect').onclick = document.getElementById('LOGIN').onclick;
}
