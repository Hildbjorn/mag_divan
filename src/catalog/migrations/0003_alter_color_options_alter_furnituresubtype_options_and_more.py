# Generated by Django 5.1.1 on 2024-09-12 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_color_options_alter_furnituremodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['name'], 'verbose_name': 'Цвет мебели', 'verbose_name_plural': '..Цвета мебели'},
        ),
        migrations.AlterModelOptions(
            name='furnituresubtype',
            options={'ordering': ['name'], 'verbose_name': 'Подтип мебели', 'verbose_name_plural': '....Подтипы мебели'},
        ),
        migrations.AlterModelOptions(
            name='furnituretype',
            options={'ordering': ['name'], 'verbose_name': 'Тип мебели', 'verbose_name_plural': '.....Типы мебели'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Фото мебели', 'verbose_name_plural': '.Фото мебели'},
        ),
    ]
