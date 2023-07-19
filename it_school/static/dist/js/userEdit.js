makeLayer('blank-wallet', 'edit-wallet', 'wrapper-blank-close-btn-wallet')

document.getElementById('edit-profile').onclick = function() {
  var deleteConfBlank = document.getElementById('blank-profile');

  if (deleteConfBlank.style.display == 'none') {
    deleteConfBlank.style.display = 'flex';
    deleteConfBlank.style.zIndex = 1;
  } else {
    deleteConfBlank.style.display = 'none';
    deleteConfBlank.style.zIndex = -999
  }
}
document.getElementById('wrapper-blank-close-btn-edit-profile').onclick = function hide() {
  var WalletBlank = document.getElementById('blank-profile');
  WalletBlank.style.display = 'none';
  WalletBlank.style.zIndex = -999;
}