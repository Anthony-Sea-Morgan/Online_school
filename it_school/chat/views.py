from django.shortcuts import render
from mainpage.models import Lesson


# Create your views here.

def chat_room(request, room_name):
    lesson = Lesson.objects.get(pk=room_name)
    return render(request, 'chat/lobby.html', {
        'room_name': room_name,
        'lesson': lesson
    })
