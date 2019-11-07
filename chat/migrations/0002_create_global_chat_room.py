from django.db import migrations


def create_global_chat_room(apps, schema_editor):
    chat_room_model_class = apps.get_model('chat', 'ChatRoom')
    chat_room_model_class(name='global').save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_global_chat_room),
    ]
