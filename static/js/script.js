function openLoginForm() {
  document.body.classList.add("showLoginForm");
}
function closeLoginForm() {
  document.body.classList.remove("showLoginForm");
}

function openRegisterForm() {
  document.body.classList.add("showRegisterForm");
}
function closeRegisterForm() {
  document.body.classList.remove("showRegisterForm");
}

function openPasswordForm() {
  document.body.classList.add("showPasswordForm");
}
function closePasswordForm() {
  document.body.classList.remove("showPasswordForm");
}

function openContentForm() {
  document.body.classList.add("showContentForm");
}
function closeContentForm() {
  document.body.classList.remove("showContentForm");
}

document.addEventListener('DOMContentLoaded', function () {
  var someElement = document.querySelector('#someElement');
})
window.onscroll = function () {
  //TOP
  if (someElement.getBoundingClientRect().top <= 0) {
    document.body.classList.remove("contentOverlay");
    closeContentForm();
  }
  //BOTTOM
  if (someElement.getBoundingClientRect().bottom <= 0) {
    document.body.classList.add("contentOverlay");
    openContentForm();
  }
}
