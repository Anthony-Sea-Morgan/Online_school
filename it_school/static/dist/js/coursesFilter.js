var technologyFilter = document.getElementById('technology-filter');
var difficultyFilter = document.getElementById('difficulty-filter');
var mentorsFilter = document.getElementById('mentors-filter') ?? undefined;

function handleFilterChange() {
  var selectedTechnology = technologyFilter.value;
  var selectedDifficulty = difficultyFilter.value;
  var selectedMentor = mentorsFilter?.value ?? 'Все менторы';

const results = document.querySelectorAll('.courses-unit-wrapper, .courses-list-manage-outer');

if (results?.length > 0) {
  results.forEach(function(result) {
  });
} else {
  return;
}

  results.forEach(function(result) {
    var technology = result.getAttribute('data-technology');
    var difficulty = result.getAttribute('data-difficulty');
    var mentor = result.querySelector('.courses-list-manage-mentor')?.textContent.trim();
    var technologyMatch = selectedTechnology === 'Все технологии' || (technology && technology.split(', ').includes(selectedTechnology));
    var difficultyMatch = selectedDifficulty === 'Любая сложность' || difficulty === selectedDifficulty;
    var mentorMatch = selectedMentor === 'Все менторы' || mentor === selectedMentor;

    if (technologyMatch && difficultyMatch && mentorMatch) {
      result.style.display = 'inline-block';
    } else {
      result.style.display = 'none';
    }
  });
}

technologyFilter.addEventListener('change', handleFilterChange);
difficultyFilter.addEventListener('change', handleFilterChange);
if (mentorsFilter) {
  mentorsFilter.addEventListener('change', handleFilterChange);
}