# Generated by Django 5.0 on 2023-12-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.TextField(default='anonym', max_length=50),
        ),
    ]
