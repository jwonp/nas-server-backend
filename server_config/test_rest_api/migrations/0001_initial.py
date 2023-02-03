# Generated by Django 4.1.3 on 2023-01-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_title', models.CharField(db_column='b_title', max_length=255)),
                ('b_writer', models.CharField(db_column='b_writer', max_length=50)),
                ('b_date', models.DateTimeField(db_column='b_date')),
            ],
            options={
                'db_table': 'board',
                'managed': False,
            },
        ),
    ]
