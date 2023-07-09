var technologyFilter = document.getElementById('technology-filter');
var difficultyFilter = document.getElementById('difficulty-filter');

 function handleFilterChange() {
        var selectedTechnology = technologyFilter.value;
        var selectedDifficulty = difficultyFilter.value;
        if (document.querySelectorAll('.courses-unit-wrapper')){
        var results = document.querySelectorAll('.courses-unit-wrapper');
        } else if (document.querySelectorAll('.courses-list-manage-outer')){
        var results = document.querySelectorAll('.courses-list-manage-outer');
        }
        results.forEach(function(result) {
            var technology = result.getAttribute('data-technology');
            var difficulty = result.getAttribute('data-difficulty');
            var technologyMatch = selectedTechnology === 'Все технологии' || technology.split(', ').includes(selectedTechnology);
            var difficultyMatch = selectedDifficulty === 'Любая сложность' || difficulty === selectedDifficulty;
            if (technologyMatch && difficultyMatch) {
                result.style.display = 'inline-block';
            } else {
                result.style.display = 'none';
            }
        });
    }
    technologyFilter.addEventListener('change', handleFilterChange);
    difficultyFilter.addEventListener('change', handleFilterChange);

