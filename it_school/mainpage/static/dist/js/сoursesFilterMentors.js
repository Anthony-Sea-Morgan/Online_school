document.addEventListener('DOMContentLoaded', function() {
  populateMentorsFilter();
});

function populateMentorsFilter() {
  var mentorsFilter = document.getElementById('mentors-filter');

  if (mentorsFilter) {
    var mentors = document.querySelectorAll('.courses-list-manage-mentor');
    var uniqueMentors = new Set();

    mentors.forEach(function(mentor) {
      var mentorName = mentor.textContent.trim();
      
      if (mentorName && !uniqueMentors.has(mentorName) && !(mentorName == 'Ментор:')) {
        var option = document.createElement('option');
        option.value = mentorName;
        option.textContent = mentorName;
        mentorsFilter.appendChild(option);
        uniqueMentors.add(mentorName);
      }
    });
  }
}