from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from mainpage.models import Course, CustomGroup, Lesson, Attendance
from registration.models import CustomUser


# Сигналы Django
@receiver(m2m_changed, sender=CustomUser.courses.through)
def handle_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Функция выполняется когда пользователю добавляется курс
    :param sender: источник сигнала
    :param instance: конкретный пользователь
    :param action: действие  - добавление связей
    :param reverse: обратная связь
    :param model: модель с которой связывают
    :param pk_set: множество ключей с колторыми связывают
    :param kwargs: прочие параметры
    :return: нет
    """
    if action == 'post_add':
        # Обработка добавления курса
        for pk in pk_set:
            course = model.objects.get(pk=pk)
            try:
                group = CustomGroup.objects.get(course_owner=pk)
                lessons = Lesson.objects.filter(course_owner=course.pk)
                # Добавить в группу пользователя
                group.users.add(instance)
                print(f'Пользователь {instance.username} записался на курс {course.title} в группу {group.name}')
                for lesson in lessons:
                    if lesson is not None and group is not None and instance is not None:
                        Attendance.objects.get_or_create(lesson=lesson, group=group, student=instance)

            except Exception as e:
                print(f'Не найдена группа для курса {str(e)}')

    elif action == 'post_remove':
        # Обработка удаления курса
        for pk in pk_set:
            course = model.objects.get(pk=pk)
            lessons = Lesson.objects.filter(course_owner=course.pk)
            for lesson in lessons:
                Attendance.objects.filter(lesson=lesson, student=instance).delete()
            # Выполнить нужные действия после удаления курса
            if course is not None:
                print(f'Пользователь {instance.username} отписался с курса {course.title}')


@receiver(pre_save, sender=Course)
def update_lessons_mentor(sender, instance, **kwargs):
    if instance.pk:  # Проверяем, что модель уже существует (не новая)
        previous_mentor = Course.objects.get(pk=instance.pk).mentor  # Получаем предыдущего ментора
        if previous_mentor != instance.mentor:  # Если ментор изменился
            lessons = Lesson.objects.filter(course_owner=instance)
            for lesson in lessons:
                lesson.mentor_owner = instance.mentor
                lesson.save()


@receiver(post_save, sender=Lesson)
def create_attendance(sender, instance, created, **kwargs):
    if created:
        group = CustomGroup.objects.get(course_owner=instance.course_owner)

        students = CustomUser.objects.filter(groups=group)
        if students.exists():
            attendance_objects = [Attendance(student=student, lesson=instance, group=group) for student in students]
            Attendance.objects.bulk_create(attendance_objects)
