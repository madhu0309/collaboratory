# Generated by Django 3.0.2 on 2020-03-02 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab_app', '0004_auto_20200301_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='num_vote_down',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
