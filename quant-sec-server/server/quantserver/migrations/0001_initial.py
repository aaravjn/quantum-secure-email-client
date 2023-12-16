# Generated by Django 3.2.23 on 2023-12-16 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('public_key', models.CharField(max_length=100)),
                ('salt', models.IntegerField()),
                ('hashed_password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_arrival', models.DateTimeField()),
                ('encrypted_subject', models.TextField()),
                ('encrypted_body', models.TextField()),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved', to='quantserver.users')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wrote', to='quantserver.users')),
            ],
        ),
    ]