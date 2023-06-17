# Generated by Django 4.2.2 on 2023-06-16 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0015_alter_course_days_of_week_alter_course_difficulty_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='course',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.customuser'),
        ),
    ]