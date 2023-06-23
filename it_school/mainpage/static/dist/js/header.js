document.getElementById('LOGIN').onclick = function() {
  var loginBlank = document.getElementById('reg-blank-login');

  if (loginBlank.style.display == 'none') {
    loginBlank.style.display = 'flex';
    loginBlank.style.zIndex = 1;
  } else {
    loginBlank.style.display = 'none';
    loginBlank.style.zIndex = -999
  }
};

document.getElementById('login-blank-close-btn').onclick = function hide() {
  var loginBlank = document.getElementById('reg-blank-login');
  loginBlank.style.display = 'none';
  loginBlank.style.zIndex = -999;
}