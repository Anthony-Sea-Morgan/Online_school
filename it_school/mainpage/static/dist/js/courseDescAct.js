function createDetailPiece() {
  const piece = document.createElement('div');
  piece.classList.add('course-detail-texture');
  return piece;
}

const detailContainer = document.getElementById('puzzleContainer');
const containerWidth = detailContainer.offsetWidth;
const containerHeight = detailContainer.offsetHeight;
console.log(containerWidth, containerHeight);
for (let i = 0; i < 30; i++) {
  const piece = createDetailPiece();
  detailContainer.appendChild(piece);
}

const detailPieces = document.querySelectorAll('.course-detail-texture');


detailPieces.forEach(piece => {
  const randomX = Math.floor(Math.random() * 600 + (containerWidth/2));
  const randomY = Math.floor(Math.random() * 600 + (containerHeight/4));
  piece.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${30}deg)`;
});







function scrollToAnchor(anchorId) {
  const anchor = document.getElementById(anchorId);
  if (anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
}
if (makeLayer('reg-blank-payconf', 'flex', 'confirm_payment', 'wrapper-blank-close-btn-payconf') == 0){
document.getElementById('LOGIN-redirect').onclick = document.getElementById('LOGIN').onclick;
}
