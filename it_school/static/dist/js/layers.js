function makeLayer (blank, ...args){
if (document.getElementById(blank)){
return 0;
}
blankLayer = document.getElementById(blank);
blankLayer.onclick = function hide(){
if (blankLayer.style.display == 'none') {
    blankLayer.style.display = 'flex';
    blankLayer.style.zIndex = 10;
  } else {
    blankLayer.style.display = 'none';
    blankLayer.style.zIndex = -999
  }
}
let btns = [];
for (let btn in args){
document.getElementById(btn).onclick = function hide() {
  blankLayer.style.display = 'none';
  blankLayer.style.zIndex = -999;
}
}
}
