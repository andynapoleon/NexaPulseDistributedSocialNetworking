# Generated by Django 5.0.1 on 2024-04-07 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_alter_author_host_alter_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='github',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='profileImage',
            field=models.URLField(blank=True, default='https://i.imgur.com/V4RclNb.png', max_length=500, null=True),
        ),
    ]