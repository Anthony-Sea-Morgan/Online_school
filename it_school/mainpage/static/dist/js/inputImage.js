let fileInput = document.getElementById('img');
let droparea = document.getElementById('img_area');


fileInput.addEventListener('dragenter focus click', function() {
  droparea.addClass('is-active');
});


fileInput.addEventListener('dragleave blur drop', function() {
  droparea.removeClass('is-active');
});


fileInput.addEventListener('change', function(e) {
    let src = URL.createObjectURL(this.files[0])
    let textContainer = document.getElementById('file-msg-icon');
    let siblingElement =  textContainer.nextElementSibling;
    let fileName = fileInput;
    textContainer.innerHTML = fileName.value.split('\\').pop();
    droparea.style.backgroundColor= 'rgb(255 140 0 / 22%)';


});

