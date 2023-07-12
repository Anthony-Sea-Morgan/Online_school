from django.shortcuts import render
from mainpage.models import Lesson, CustomGroup
from management.forms import LessonForm
from django.contrib.auth.decorators import login_required


@login_required  # Декоратор для требования аутентификации пользователя
def chat_room(request, room_name):
    """
    Представление для отображения комнаты чата.
    Требует аутентификации пользователя.
    Принимает запрос (request) и имя комнаты чата (room_name).
    Возвращает рендеринг шаблона 'chat/lobby.html' с переданными данными.
    """
    user = request.user
    lesson = Lesson.objects.filter(pk=room_name).first()
    group = CustomGroup.objects.get(course_owner_id=lesson.course_owner_id)
    return render(request, 'chat/lobby.html', {
        'room_name': room_name,
        'lesson': lesson,
        'user': user,
        'lesson_form': LessonForm(),
        'group': group,
    })
