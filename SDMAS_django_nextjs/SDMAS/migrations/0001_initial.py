# Generated by Django 5.1.6 on 2025-02-06 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('urgency', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('status', models.CharField(choices=[('reported', 'Reported'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='reported', max_length=20)),
                ('repair_appointment_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=100, unique=True)),
                ('floor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepairStatusUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('reported', 'Reported'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed')], max_length=20)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('repair_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMAS.repairrequest')),
            ],
        ),
        migrations.CreateModel(
            name='RepairHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repair_what', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMAS.repairstatusupdate')),
                ('room', models.ManyToManyField(to='SDMAS.room')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMAS.room')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='repairrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMAS.student'),
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technician_id', models.CharField(max_length=20, unique=True)),
                ('expertise', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='repairstatusupdate',
            name='technician',
            field=models.ManyToManyField(to='SDMAS.technician'),
        ),
        migrations.CreateModel(
            name='RepairAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('reported', 'Reported'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='assigned', max_length=20)),
                ('repair_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='SDMAS.repairrequest')),
                ('technician', models.ManyToManyField(to='SDMAS.technician')),
            ],
        ),
    ]
