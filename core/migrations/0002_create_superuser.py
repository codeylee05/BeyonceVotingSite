from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username="MasterUser").exists():
        User.objects.create_superuser(
            "MasterUser", "mleefa5002@gmail.com", "MasterUserIsCool0000")


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(create_admin)]
