# Generated by Django 4.0.3 on 2022-03-31 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnoseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=350, verbose_name='User ID')),
                ('stage', models.CharField(default='G1', max_length=350, verbose_name='Stage')),
                ('question_index', models.IntegerField(default=0, verbose_name='question index')),
                ('pre_diagnose', models.TextField(blank=True, null=True, verbose_name='Pre diagnose')),
                ('final_diagnose', models.TextField(blank=True, null=True, verbose_name='')),
            ],
            options={
                'verbose_name': 'Diagnose report',
                'verbose_name_plural': 'Diagnosis reports',
            },
        ),
        migrations.CreateModel(
            name='DiagnoseResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnose_answer', models.CharField(max_length=350, verbose_name='Diagnose answer')),
                ('diagnose_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('diagnose_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnose_report.diagnosereport', verbose_name='Diagnose report')),
            ],
            options={
                'verbose_name': 'Diagnose result',
                'verbose_name_plural': 'Diagnose results',
            },
        ),
    ]