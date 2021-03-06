# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 01:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('book_title', models.CharField(max_length=200)),
                ('book_author', models.CharField(max_length=200)),
                ('book_pub_date', models.CharField(max_length=40)),
                ('book_publisher', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('pagecount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('rating', models.IntegerField()),
                ('url', models.CharField(max_length=100)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Shelves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf', models.CharField(max_length=200)),
                ('people', models.IntegerField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Book')),
            ],
        ),
    ]
