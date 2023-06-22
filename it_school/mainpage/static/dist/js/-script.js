loginBlank = document.getElementById('reg-blank-login');

class Menu {
    constructor(elem) {
      this._elem = elem;
      elem.onclick = this.onClick.bind(this); // (*)
    }

    login() {
      loginBlank.style.display == 'none'? loginBlank.style.display = 'inherit': loginBlank.style.display = 'none';
    }

    onClick(event) {
      let action = event.target.dataset.action;
      if (action) {
        this[action]();
      } else{
      loginBlank.style.display = 'none';
      }

    }
  }

  new Menu(headerUl);



