# Generated by Django 3.1.2 on 2020-10-18 08:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_performer', models.BooleanField(default=0, null=True)),
                ('is_supervisor', models.BooleanField(default=0, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('status', models.CharField(choices=[(0, 'Планируется'), (1, 'Активная'), (2, 'Контроль'), (3, 'Завершена')], max_length=1, verbose_name='статус')),
                ('time_begin', models.DateTimeField(null=True, verbose_name='время начала')),
                ('time_end', models.DateTimeField(null=True, verbose_name='время завершения')),
                ('planned_time', models.DateTimeField(null=True, verbose_name='планируемое время завершения')),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='my_tasks', to=settings.AUTH_USER_MODEL, verbose_name='исполнитель')),
                ('supervisors', models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='наблюдатели')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст напоминания')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reminders', to='task_tracker.task', verbose_name='задача')),
                ('users', models.ManyToManyField(related_name='reminders', to=settings.AUTH_USER_MODEL, verbose_name='пользователей')),
            ],
            options={
                'verbose_name': 'Напоминание',
                'verbose_name_plural': 'Напоминания',
            },
        ),
        migrations.CreateModel(
            name='ChangeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_status', models.CharField(choices=[(0, 'Планируется'), (1, 'Активная'), (2, 'Контроль'), (3, 'Завершена')], max_length=1, verbose_name='предыдущий статус')),
                ('next_status', models.CharField(choices=[(0, 'Планируется'), (1, 'Активная'), (2, 'Контроль'), (3, 'Завершена')], max_length=1, verbose_name='следующий статус')),
                ('performer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='change_status', to=settings.AUTH_USER_MODEL, verbose_name='кем изменен')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='change_status', to='task_tracker.task', verbose_name='задача')),
            ],
            options={
                'verbose_name': 'Изменение статуса',
            },
        ),
    ]