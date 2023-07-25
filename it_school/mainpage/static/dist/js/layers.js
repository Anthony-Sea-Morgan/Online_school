

function makeLayer(blank, display='flex', ...args) {
  if (!document.getElementById(blank)) {
    return 0;
  }

  var blankLayer = document.getElementById(blank);

  for (let btn of args) {
    const button = document.getElementById(btn);
    if (button) {
      button.onclick = () => {
          if (blankLayer.style.display === 'none') {
    blankLayer.style.display = display;
    blankLayer.style.zIndex = 10;
  } else {
    blankLayer.style.display = 'none';
    blankLayer.style.zIndex = -999;
  }
      }
    }
  }
}
