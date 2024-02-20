# Generated by Django 5.0.1 on 2024-02-15 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MakesPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('pid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('public', models.BooleanField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='unknown@example.com', max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=255)),
                ('github', models.CharField(default='', max_length=100)),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='assets/profile_images/')),
            ],
        ),
        migrations.CreateModel(
            name='HasComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.makespost')),
            ],
        ),
        migrations.AddField(
            model_name='makespost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.post'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('lid', models.AutoField(primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.post')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user'),
        ),
        migrations.CreateModel(
            name='OwnLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.like')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user')),
            ],
        ),
        migrations.CreateModel(
            name='OwnComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user')),
            ],
        ),
        migrations.AddField(
            model_name='makespost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.user'),
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_set', to='authors.user')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_set', to='authors.user')),
            ],
            options={
                'unique_together': {('follower', 'followed')},
            },
        ),
        migrations.CreateModel(
            name='FollowedBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to='authors.user')),
                ('id2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='authors.user')),
            ],
            options={
                'unique_together': {('id1', 'id2')},
            },
        ),
    ]
