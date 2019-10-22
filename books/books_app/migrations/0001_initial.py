# Generated by Django 2.2.5 on 2019-10-20 22:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(blank=True, max_length=200)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author_uuid', models.UUIDField(blank=True, null=True)),
                ('reader_uuid', models.UUIDField(blank=True, null=True)),
            ],
        ),
    ]
