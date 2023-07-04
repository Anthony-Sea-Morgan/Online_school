from tabulate import tabulate
from .models import Course, Lesson, CustomGroup, CustomUser, Attendance, TECHNOLOGIES
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request):
    course_object = Course.objects.all()
    for i in course_object:
        i.img = str(i.img)[5:]
        i.imgTech = str(i.tech_img)[5:]
    data = {
        'title': 'Online school',
        'page_label': 'Главная страница',
        'courses': course_object,
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
    }
    template = 'mainpage.html'
    return render(request, template, data)


class CourseDetailView(DetailView):
    error = ''
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        if 'confirm_payment' in request.POST:
            course = self.get_object()
            user = request.user
            course_price = course.price

            if user.wallet >= course_price:
                user.wallet -= course_price
                user.save()
                messages.success(request, 'Оплата прошла успешно.')
                return redirect('purchase_confirmation', pk=course.pk)
            else:
                self.error = 'Недостаточно средств на счете.'

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.error
        if self.error:
            context['styleconfp'] = 'display: flex;'
        return context


def purchase_confirmation(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'purchase_confirmation.html', {'course': course})


def attendance_table(request):
    groups = CustomGroup.objects.all()
    attendance_tables = []

    for group in groups:
        lessons = Lesson.objects.filter(course_owner=group.course_owner)
        students = CustomUser.objects.filter(groups=group)
        attendance = Attendance.objects.filter(group=group)

        print(f'{students}')

        table = []
        table_headers = ['Слушатель'] + [str(lesson.start_date) for lesson in lessons]

        for student in students:
            row = [student.get_full_name()]
            for lesson in lessons:
                attendance_entry = attendance.get(lesson=lesson, student=student)
                row.append(attendance_entry.attended)
            table.append(row)

        attendance_tables.append({
            'group': group,
            'table': tabulate(table, headers=table_headers, tablefmt='grid')
        })

    return render(request, 'attendance.html', {'attendance_tables': attendance_tables})
