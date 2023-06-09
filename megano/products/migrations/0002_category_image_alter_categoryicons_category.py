# Generated by Django 4.2.1 on 2023-06-04 15:57

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(null=True, upload_to=products.models.category_image_directory_path, verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='categoryicons',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.category', verbose_name='категория'),
        ),
    ]