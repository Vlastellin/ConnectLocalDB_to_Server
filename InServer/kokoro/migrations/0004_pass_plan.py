# Generated by Django 3.1 on 2020-09-08 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kokoro', '0003_auto_20200908_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='pass',
            name='plan',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
