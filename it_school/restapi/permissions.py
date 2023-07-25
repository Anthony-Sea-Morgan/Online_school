from rest_framework.permissions import BasePermission
from mainpage.models import Lesson

class IsCourseOwner(BasePermission):
    def has_permission(self, request, view):
        lesson_id = view.kwargs.get('lesson_id')
        if lesson_id is not None:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                return False

            # Check if the course associated with the lesson exists in the user's list of courses
            return request.user.courses.filter(id=lesson.course_owner.id).exists()

        return False
