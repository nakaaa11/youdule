# Generated by Django 4.0.4 on 2022-06-09 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdule', '0005_alter_streamer_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='channel_id',
            field=models.CharField(max_length=24, null=True),
        ),
    ]