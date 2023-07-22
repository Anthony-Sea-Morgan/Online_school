let descriptionFull = document.getElementsByClassName('description-content')[0];
descriptionFull.innerHTML = descriptionFull.innerText;
function scrollToAnchor(anchorId) {
  const anchor = document.getElementById(anchorId);
  if (anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
}
if (makeLayer('reg-blank-payconf', 'confirm_payment', 'wrapper-blank-close-btn-payconf') == 0){
} else{
document.getElementById('LOGIN-redirect').onclick = document.getElementById('LOGIN').onclick;
}
