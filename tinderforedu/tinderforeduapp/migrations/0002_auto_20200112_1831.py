# Generated by Django 3.0.2 on 2020-01-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinderforeduapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='good_subject',
            field=models.ManyToManyField(related_name='Userinfos', to='tinderforeduapp.Subject'),
        ),
    ]