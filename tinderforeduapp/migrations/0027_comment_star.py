# Generated by Django 3.0 on 2020-02-23 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinderforeduapp', '0026_auto_20200223_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='star',
            field=models.CharField(max_length=500, null=True),
        ),
    ]