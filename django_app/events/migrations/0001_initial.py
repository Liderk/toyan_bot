# Generated by Django 4.2.17 on 2024-12-28 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('event_type', models.SmallIntegerField(choices=[(1, 'Тренировка'), (2, 'Сбор')], verbose_name='Тип события')),
                ('descriptions', models.CharField(max_length=1500, verbose_name='Описание')),
                ('location', models.CharField(max_length=250, verbose_name='Место проведения')),
                ('organizers', models.CharField(max_length=250, verbose_name='Организаторы')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата окончания')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('descriptions', models.CharField(max_length=1000, verbose_name='Описание')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата окончания')),
                ('organizers', models.CharField(max_length=250, verbose_name='Организаторы')),
                ('big', models.BooleanField(default=False, verbose_name='Большая игра')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('game_area', models.CharField(max_length=50, verbose_name='Полигон')),
                ('side_commander', models.CharField(blank=True, max_length=50, null=True, verbose_name='Командующий стороны')),
                ('judas_commander', models.CharField(blank=True, max_length=50, null=True, verbose_name='Командующий Иудой')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
        migrations.CreateModel(
            name='NotificationPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.SmallIntegerField(choices=[(1, 'Час'), (2, 'День'), (3, 'Неделя'), (4, 'Месяц')], verbose_name='Период')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Период уведомления',
                'verbose_name_plural': 'Период уведомлений',
            },
        ),
        migrations.CreateModel(
            name='GameEventNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('notified', models.BooleanField(default=False, verbose_name='Уведомление отправлено')),
                ('notification_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата уведомления')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('notification_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedulers', to='events.notificationperiod', verbose_name='Период уведомления')),
            ],
            options={
                'verbose_name': 'Расписание уведомления',
                'verbose_name_plural': 'Расписание уведомлений',
            },
        ),
    ]
