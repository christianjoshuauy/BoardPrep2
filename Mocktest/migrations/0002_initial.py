# Generated by Django 4.2.4 on 2024-01-09 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Course', '0001_initial'),
        ('Class', '0002_initial'),
        ('Mocktest', '0001_initial'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mocktestscores',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_scores', to='User.student'),
        ),
        migrations.AddField(
            model_name='mocktest',
            name='classID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.class'),
        ),
        migrations.AddField(
            model_name='mocktest',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.course'),
        ),
        migrations.AddField(
            model_name='mockquestions',
            name='difficulty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mocktest.difficulty'),
        ),
        migrations.AddField(
            model_name='mockquestions',
            name='mocktest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mockquestions', to='Mocktest.mocktest'),
        ),
        migrations.AddField(
            model_name='correctquestions',
            name='mockquestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mocktest.mockquestions'),
        ),
        migrations.AddField(
            model_name='correctquestions',
            name='mocktest_score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mocktest.mocktestscores'),
        ),
        migrations.AlterUniqueTogether(
            name='mocktestscores',
            unique_together={('mocktest_id', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='correctquestions',
            unique_together={('mocktest_score', 'mockquestion')},
        ),
    ]
