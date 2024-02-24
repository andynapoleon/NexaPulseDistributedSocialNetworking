# Generated by Django 5.0.1 on 2024-02-23 23:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', max_length=20)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends'), ('UNLISTED', 'Unlisted')], default=('PUBLIC', 'Public'), max_length=20)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.CharField(default='', max_length=50)),
                ('content', models.TextField(default='')),
                ('authorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
            ],
        ),
    ]
