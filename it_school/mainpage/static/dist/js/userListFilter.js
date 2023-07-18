  document.addEventListener('DOMContentLoaded', function() {});
    const searchInput = document.getElementById('search-input');
    const userTable = document.getElementById('user-table');
    const userRows = userTable.getElementsByClassName('user-row');

    function filterUsers() {
      const searchText = searchInput.value.toLowerCase();

      for (let i = 0; i < userRows.length; i++) {
        const userRow = userRows[i];
        const username = userRow.cells[0].querySelector('.past-lesson input[type="text"]').value.toLowerCase();
        const email = userRow.cells[1].querySelector('.past-lesson input[type="email"]').value.toLowerCase();
        const mentor = userRow.cells[3].querySelector('.past-lesson label').innerHTML.toLowerCase();
        const staff = userRow.cells[5].querySelector('.past-lesson label').innerHTML.toLowerCase();
        const superuser = userRow.cells[6].querySelector('.past-lesson label').innerHTML.toLowerCase();

        if (
          username.includes(searchText) ||
          email.includes(searchText) ||
          mentor.includes(searchText) ||
          staff.includes(searchText) ||
          superuser.includes(searchText)
        ) {
          userRow.style.display = '';
        } else {
          userRow.style.display = 'none';
        }
      }
    }

    searchInput.addEventListener('input', filterUsers);


userTable.addEventListener('change', function(event) {
  const target = event.target;

  if (target.classList.contains('mentor-checkbox')) {
    const roleLabel = target.nextElementSibling;

    if (target.checked) {
      roleLabel.textContent = 'Ментор';
    } else {
      roleLabel.textContent = 'Студент';
    }
  } else if (target.classList.contains('staff-checkbox')) {
  const roleLabel = target.nextElementSibling;
  if (target.checked) {
      roleLabel.textContent = 'Стаф';
    } else {
      roleLabel.textContent = 'Юзер';
    }
  } else if(target.classList.contains('superuser-checkbox')) {
  const roleLabel = target.nextElementSibling;
  if (target.checked) {
      roleLabel.textContent = 'Суперюзер';
    } else {
      roleLabel.textContent = 'Юзер';
    }
  }
});