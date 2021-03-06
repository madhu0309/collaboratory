# Generated by Django 3.0.2 on 2020-02-10 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formset_app', '0002_auto_20200208_0413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', to='formset_app.Book')),
            ],
            options={
                'db_table': 'author',
            },
        ),
    ]
