 var selectedDates = [];
function Calendar(id, year, month) {
var Dlast = new Date(year,month+1,0).getDate(),
    D = new Date(year,month,Dlast),
    DNlast = new Date(D.getFullYear(),D.getMonth(),Dlast).getDay(),
    DNfirst = new Date(D.getFullYear(),D.getMonth(),1).getDay(),
    calendar = '<tr>',
    month=["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"];
if (DNfirst != 0) {
  for(var  i = 1; i < DNfirst; i++) calendar += '<td>';
}else{
  for(var  i = 0; i < 6; i++) calendar += '<td>';
}
for(var  i = 1; i <= Dlast; i++) {
  if (i == new Date().getDate() && D.getFullYear() == new Date().getFullYear() && D.getMonth() == new Date().getMonth()) {
    calendar += '<td class="today">' + i;
  }else{
    calendar += '<td>' + i;
  }
  if (new Date(D.getFullYear(),D.getMonth(),i).getDay() == 0) {
    calendar += '<tr>';
  }
}
for(var  i = DNlast; i < 7; i++) calendar += '<td>&nbsp;';
document.querySelector('#'+id+' tbody').innerHTML = calendar;
document.querySelector('#'+id+' thead td:nth-child(2)').innerHTML = month[D.getMonth()] +' '+ D.getFullYear();
document.querySelector('#'+id+' thead td:nth-child(2)').dataset.month = D.getMonth();
document.querySelector('#'+id+' thead td:nth-child(2)').dataset.year = D.getFullYear();
if (document.querySelectorAll('#'+id+' tbody tr').length < 6) {  // чтобы при перелистывании месяцев не "подпрыгивала" вся страница, добавляется ряд пустых клеток. Итог: всегда 6 строк для цифр
    document.querySelector('#'+id+' tbody').innerHTML += '<tr><td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;';
}
 highlightCalendarDays();
}
Calendar("calendar", new Date().getFullYear(), new Date().getMonth());
// переключатель минус месяц
document.querySelector('#calendar thead tr:nth-child(1) td:nth-child(1)').onclick = function() {
  Calendar("calendar", document.querySelector('#calendar thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar thead td:nth-child(2)').dataset.month)-1);
}
// переключатель плюс месяц
document.querySelector('#calendar thead tr:nth-child(1) td:nth-child(3)').onclick = function() {
  Calendar("calendar", document.querySelector('#calendar thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar thead td:nth-child(2)').dataset.month)+1);
}




 function highlightCalendarDays() {
        var calendarDays = document.querySelectorAll('.personal-calendar td');

        calendarDays.forEach(function (calendarDay) {
            var calendarDate = new Date(
                document.querySelector('#calendar thead td:nth-child(2)').dataset.year,
                parseFloat(document.querySelector('#calendar thead td:nth-child(2)').dataset.month),
                parseInt(calendarDay.textContent, 10)
            );

            // Добавляем время в 00:00, чтобы сравнивать только даты
            calendarDate.setHours(0, 0, 0, 0);

            // Если дата есть в списке выбранных, то выделяем ячейку календаря
            if (selectedDates.includes(calendarDate.getTime())) {
                calendarDay.style.background = 'rgba(255, 165, 0, 0.5)'; // Измените на любой другой стиль выделения
            } else {
                calendarDay.style.background = 'none';
            }
        });
    }

    function parseCustomDate(dateString) {
    var dateParts = dateString.split(' ');
    var month = dateParts[0];
    var day = parseInt(dateParts[1].replace(',', ''), 10);
    var year = parseInt(dateParts[2], 10);
    var months = {
      'Jan.': 0, 'Feb.': 1, 'Mar.': 2, 'Apr.': 3,
      'May': 4, 'Jun.': 5, 'July': 6, 'Aug.': 7,
      'Sep.': 8, 'Oct.': 9, 'Nov.': 10, 'Dec.': 11
    };
    var monthIndex = months[month];
    return new Date(year, monthIndex, day);
  }

    // Получаем все даты из групп уроков
    var lessonDates = document.querySelectorAll('.date-unit-wrapper.ib.va h4');

    lessonDates.forEach(function (lessonDate) {
        var date = parseCustomDate(lessonDate.textContent.trim());

        // Добавляем время в 00:00, чтобы сравнивать только даты
        date.setHours(0, 0, 0, 0);

        // Сохраняем выбранную дату в список
        selectedDates.push(date.getTime());
    });

    // Вызываем функцию для выделения ячеек в календаре
    highlightCalendarDays();