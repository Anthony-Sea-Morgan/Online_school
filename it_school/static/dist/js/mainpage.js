let pieceDetail = ['╳','▷','☐','│','○','●','◣','◜']
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
  piece.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${30}deg)`;
  piece.style.fontSize = `${Math.floor(Math.random()%10*200)}px`;
});