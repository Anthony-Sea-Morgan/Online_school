let descriptionFull = document.getElementsByClassName('description-content')[0];
descriptionFull.innerHTML = descriptionFull.innerText;
function scrollToAnchor(anchorId) {
  const anchor = document.getElementById(anchorId);
  if (anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
}
if (document.getElementById('confirm_payment')){
document.getElementById('confirm_payment').onclick = function() {
  var payConfBlank = document.getElementById('reg-blank-payconf');

  if (payConfBlank.style.display == 'none') {
    payConfBlank.style.display = 'flex';
    payConfBlank.style.zIndex = 1;
  } else {
    payConfBlank.style.display = 'none';
    payConfBlank.style.zIndex = -999
  }
}} else{
document.getElementById('LOGIN-redirect').onclick = document.getElementById('LOGIN').onclick;
}
document.getElementById('wrapper-blank-close-btn-payconf').onclick = function hide() {
  var loginBlank = document.getElementById('reg-blank-payconf');
  loginBlank.style.display = 'none';
  loginBlank.style.zIndex = -999;
}