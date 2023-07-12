let fileInput = document.getElementById('img');
let droparea = document.getElementById('img_area');
let fileInputIcon = document.getElementById('img_tech');
let dropareaIcon = document.getElementById('img_tech_area');


fileInput.addEventListener('dragenter focus click', function() {
  droparea.addClass('is-active');
});


fileInput.addEventListener('dragleave blur drop', function() {
  droparea.removeClass('is-active');
});


fileInput.addEventListener('change', function(e) {
    let src = URL.createObjectURL(this.files[0])
    let textContainer = document.getElementById('file-msg-icon');
    let fileName = fileInput;
    textContainer.innerHTML = fileName.value.split('\\').pop();
    droparea.style.backgroundColor= 'rgb(255 140 0 / 22%)';


});



fileInputIcon.addEventListener('dragenter focus click', function() {
  dropareaIcon.addClass('is-active');
});


fileInputIcon.addEventListener('dragleave blur drop', function() {
  dropareaIcon.removeClass('is-active');
});


fileInputIcon.addEventListener('change', function(e) {
    let src = URL.createObjectURL(this.files[0])
    let textContainer = document.getElementById('file-msg-icon-tech');
    let fileName = fileInputIcon;
    textContainer.innerHTML = fileName.value.split('\\').pop();
    dropareaIcon.style.backgroundColor= 'rgb(255 140 0 / 22%)'
});

