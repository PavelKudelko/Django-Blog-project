# Generated by Django 5.0 on 2024-01-07 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='snippet',
            field=models.CharField(default='Default snippet', max_length=200),
        ),
    ]