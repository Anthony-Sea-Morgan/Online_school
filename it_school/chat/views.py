from django.shortcuts import render
from mainpage.models import Lesson
from django.contrib.auth.decorators import login_required


@login_required  # Декоратор для требования аутентификации пользователя
def chat_room(request, room_name):
    user = request.user
    lesson = Lesson.objects.filter(pk=room_name).first()
    return render(request, 'chat/lobby.html', {
        'room_name': room_name,
        'lesson': lesson,
        'user': user
    })
