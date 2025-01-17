# Generated by Django 5.1.2 on 2024-10-30 10:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_enquiery_description_alter_enquiery_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiery',
            name='event',
        ),
        migrations.RemoveField(
            model_name='enquiery',
            name='user',
        ),
        migrations.AddField(
            model_name='bookevent',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event'),
        ),
    ]
