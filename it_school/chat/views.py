from django.shortcuts import render, get_object_or_404
from mainpage.models import Lesson, CustomGroup
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
    course_id = lesson.course_owner_id
    is_group_member = lesson.course_owner.group_course.filter(users=user).exists()
    if not (lesson or is_group_member):
        # Если пользователь не является владельцем курса и не является членом группы-владельца,
        # то перенаправляем его на другую страницу или показываем сообщение об ошибке.
        return render(request, 'access_deny.html')



    # Проверяем, является ли пользователь владельцем курса
    is_course_owner = lesson.course_owner.mentor == user
    group = get_object_or_404(CustomGroup, course_owner_id=course_id)
    # Проверяем, является ли пользователь членом группы-владельца курса




    return render(request, 'chat/lobby.html', {
        'room_name': room_name,
        'lesson': lesson,
        'user': user,
        'group': group,
    })
