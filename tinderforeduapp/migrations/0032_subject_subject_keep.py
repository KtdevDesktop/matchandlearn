# Generated by Django 3.0.4 on 2020-03-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinderforeduapp', '0031_userinfo_fb_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_keep',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
