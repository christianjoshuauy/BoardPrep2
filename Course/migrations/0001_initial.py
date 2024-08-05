# Generated by Django 4.2.4 on 2024-01-09 18:55

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('course_title', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=500)),
                ('long_description', models.TextField()),
                ('image', models.ImageField(default='default.png', upload_to='images/')),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('syllabus_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus', to='Course.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lesson_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('lesson_title', models.CharField(max_length=200)),
                ('order', models.IntegerField(help_text='Order of the lesson in the syllabus')),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='Course.syllabus')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField(help_text='Page number within the lesson')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Content')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='Course.lesson')),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages_by_syllabus', to='Course.syllabus')),
            ],
            options={
                'ordering': ['page_number'],
                'unique_together': {('lesson', 'page_number')},
            },
        ),
    ]
