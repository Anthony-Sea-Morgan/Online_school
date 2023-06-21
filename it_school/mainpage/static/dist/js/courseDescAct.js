let descriptionFull = document.getElementsByClassName('description-content')[0];
descriptionFull.innerHTML = descriptionFull.innerText;
function scrollToAnchor(anchorId) {
  const anchor = document.getElementById(anchorId);
  if (anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
}