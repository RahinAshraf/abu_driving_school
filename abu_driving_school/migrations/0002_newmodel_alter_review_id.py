# Generated by Django 4.2.16 on 2025-03-18 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abu_driving_school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
