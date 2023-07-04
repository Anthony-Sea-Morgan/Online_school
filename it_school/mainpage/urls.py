from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path
import registration.views
from .views import CourseDetailView, purchase_confirmation, index, attendance_table, chat_room, send_message
from registration.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', index, name='index'),
    # В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    path('api/', include('restapi.urls')),
    path('<int:pk>', CourseDetailView.as_view(), name='course_detail'),
    path('attendance/', attendance_table, name='attendance_table'),
    path('purchase_confirmation/<int:pk>/', purchase_confirmation, name='purchase_confirmation'),
    path('room/<int:group_id>/', chat_room, name='chat_room'),
    path('room/<int:group_id>/send_message/', send_message, name='send_message'),

]
