from celery import shared_task
from django.core.mail import send_mail
from datetime import date
from registration.models import CustomUser
from mainpage.models import Lesson, LessonRegistration
from django.utils import timezone
import logging

@shared_task
def send_reminder_email_task():
    # Получаем текущую дату и время
    current_datetime = timezone.now()

    # Получаем все предстоящие занятия, которые начинаются через 1 час или позже
    upcoming_lessons = Lesson.objects.filter(start_date__gte=current_datetime + timezone.timedelta(days=1-7))

    # Для каждого предстоящего занятия, получаем студентов, которые записаны на это занятие
    for lesson in upcoming_lessons:
        registered_students = CustomUser.objects.filter(lessonregistration__lesson=lesson)

        # Отправляем электронное письмо каждому студенту с напоминанием о занятии
        for student in registered_students:
            subject = f"Напоминание о занятии: {lesson.title}"
            message = f"Уважаемый(ая) {student.first_name} {student.last_name},\n\n" \
                      f"Напоминаем вам о предстоящем занятии:\n" \
                      f"Курс: {lesson.title}\n" \
                      f"Дата и время: {lesson.start_date} {lesson.start_time}\n" \
                      f"Ментор: {lesson.mentor}\n\n" \
                      f"Желаем успешного занятия!\n" \
                      f"Команда Online School"
            from_email = "norepy.onlinecourses@gmail.com"
            recipient_list = [student.email]

            send_mail(subject, message, from_email, recipient_list)

def send_email_to_student(user_email, lesson_title, lesson_start_date):
    subject = "Reminder: Upcoming Lesson"
    message = f"Dear student, you have an upcoming lesson titled '{lesson_title}' on {lesson_start_date}. Don't forget to attend!"
    from_email = "norepy.onlinecourses@gmail.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

