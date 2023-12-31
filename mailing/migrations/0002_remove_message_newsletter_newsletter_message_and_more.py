# Generated by Django 4.2.3 on 2023-08-20 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='newsletter',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение'),
        ),
        migrations.AlterField(
            model_name='deliverylog',
            name='status',
            field=models.CharField(choices=[('SC', 'Успешно'), ('FD', 'Провалено')], max_length=15, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='frequency',
            field=models.CharField(choices=[('ED', 'Раз в день'), ('EW', 'Раз в неделю'), ('EM', 'Раз в месяц')], max_length=20, verbose_name='частота рассылки'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('CR', 'Создана'), ('ST', 'Запущена'), ('CMP', 'Заврешена')], max_length=10, verbose_name='статус рассылки'),
        ),
    ]
