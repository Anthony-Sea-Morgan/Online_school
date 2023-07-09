document.getElementById('delete-btn').onclick = function() {
  var deleteConfBlank = document.getElementById('blank-delete');

  if (deleteConfBlank.style.display == 'none') {
    deleteConfBlank.style.display = 'flex';
    deleteConfBlank.style.zIndex = 1;
  } else {
    deleteConfBlank.style.display = 'none';
    deleteConfBlank.style.zIndex = -999
  }
}
document.getElementById('wrapper-blank-close-btn-delete').onclick = function hide() {
  var loginBlank = document.getElementById('blank-delete');
  loginBlank.style.display = 'none';
  loginBlank.style.zIndex = -999;
}
document.getElementById('blank-delete-no').onclick = document.getElementById('wrapper-blank-close-btn-delete').onclick
