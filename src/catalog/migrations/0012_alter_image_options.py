# Generated by Django 5.1.1 on 2024-09-14 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_furnituremodel_colors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['furniture_model', '-uploaded_at'], 'verbose_name': 'Фото мебели', 'verbose_name_plural': 'Фото мебели'},
        ),
    ]
