from celery import shared_task
from django.core.mail import send_mail
from datetime import date
from registration.models import CustomUser
from mainpage.models import Lesson
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_email_task():
    logger.info("Начало отправки напоминания по электронной почте")

    # Получаем текущую дату и время
    current_datetime = timezone.now()

    # Получаем все предстоящие занятия, которые начинаются через 1 час или позже, отсортированные по start_date
    upcoming_lessons = Lesson.objects.filter(start_date__gte=current_datetime + timezone.timedelta(days=1)).order_by('start_date')

    # Получаем только первые два ближайших занятия
    upcoming_lessons = upcoming_lessons[:2]

    # Отправляем электронное письмо каждому студенту с напоминанием о занятии
    for lesson in upcoming_lessons:
        logger.info(f"Отправка напоминания для занятия: {lesson.title}")

        # Получаем студентов, которые записаны на это занятие
        registered_students = CustomUser.objects.filter(is_student=True, courses=lesson.course_owner)

        # Отправка писем только студентам, а не менторам
        for student in registered_students:
            logger.info(f"Отправка напоминания для студента: {student.first_name} {student.last_name}")
            subject = f"Напоминание о занятии: {lesson.title}"
            message = f"Уважаемый(ая) {student.first_name} {student.last_name},\n\n" \
                      f"Напоминаем вам о предстоящем занятии:\n" \
                      f"Курс: {lesson.title}\n" \
                      f"Дата и время: {lesson.start_date} {lesson.start_time}\n" \
                      f"Ментор: {lesson.mentor_owner}\n\n" \
                      f"Желаем успешного занятия!\n" \
                      f"Команда Online School"
            from_email = "noreply.onlinecourses@gmail.com"
            recipient_list = [student.email]

            # Отправка письма и логирование результата
            try:
                send_mail(subject, message, from_email, recipient_list)
                logger.info(f"Напоминание успешно отправлено для студента {student}")
            except Exception as e:
                logger.error(f"Ошибка при отправке напоминания для студента {student}: {str(e)}")

    logger.info("Завершение задачи send_reminder_email_task")
