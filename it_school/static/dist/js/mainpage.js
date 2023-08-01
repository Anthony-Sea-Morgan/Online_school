let pieceDetail = ['╳','▷','☐','│','○','●','◣']
function createDetailPiece() {
  const piece = document.createElement('div');
  piece.classList.add('mainpage-detail-texture');
  piece.innerHTML = pieceDetail[Math.floor(Math.random()* pieceDetail.length)]

  return piece;
}

const detailContainer = document.getElementById('puzzleContainer');
const containerWidth = detailContainer.offsetWidth;
const containerHeight = detailContainer.offsetHeight;
for (let i = 0; i < 40; i++) {
  const piece = createDetailPiece();
  detailContainer.appendChild(piece);
}

const detailPieces = document.querySelectorAll('.mainpage-detail-texture');


detailPieces.forEach(piece => {
  const randomX = Math.floor(Math.random() *  (containerWidth/1.8));
  const randomY = Math.floor(Math.random() *  (containerHeight));
  piece.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${Math.random()*360}deg)`;
  piece.style.fontSize = `${Math.floor((Math.random()%10+5)*10)}px`;
});

function movePiecesSlowly() {
  detailPieces.forEach(piece => {
    const randomX = Math.floor(Math.random() * (containerWidth / 1.8));
    const randomY = Math.floor(Math.random() * containerHeight);
    const randomRotation = Math.random() * 360;

    let currentX = containerWidth;
    let currentY = containerHeight;
    let currentRotation = 0;

    const moveInterval = setInterval(() => {
      const deltaX = (randomX - currentX) * 0.1;
      const deltaY = (randomY - currentY) * 0.1;
      const deltaRotation = (randomRotation - currentRotation) * 0.1;

      currentX += deltaX;
      currentY += deltaY;
      currentRotation += deltaRotation;

      // Вычисляем смещение по X и Y в зависимости от угла вращения
      const offsetX = Math.cos((currentRotation + 90) * Math.PI / 180) * 100;
      const offsetY = Math.sin((currentRotation + 90) * Math.PI / 180) * 100;

      piece.style.transform = `translate(${currentX + offsetX}px, ${currentY + offsetY}px) rotate(${currentRotation}deg)`;

      if (Math.abs(randomX - currentX) < 1 && Math.abs(randomY - currentY) < 1 && Math.abs(randomRotation - currentRotation) < 1) {
        clearInterval(moveInterval);
      }
    }, 50);
  });
}

movePiecesSlowly();
