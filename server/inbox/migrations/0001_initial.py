# Generated by Django 5.0.1 on 2024-03-18 20:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0002_initial'),
        ('follow', '0001_initial'),
        ('likes', '0001_initial'),
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('authorId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_likes', models.ManyToManyField(blank=True, to='likes.commentlikes')),
                ('comments', models.ManyToManyField(blank=True, to='comments.comment')),
                ('follow_requests', models.ManyToManyField(blank=True, to='follow.follows')),
                ('post_likes', models.ManyToManyField(blank=True, to='likes.postlikes')),
                ('posts', models.ManyToManyField(blank=True, to='posts.post')),
            ],
        ),
    ]
