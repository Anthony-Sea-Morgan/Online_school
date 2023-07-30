
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
