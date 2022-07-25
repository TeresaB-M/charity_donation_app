# Generated by Django 4.0.5 on 2022-07-23 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_donation_app', '0004_donation_is_taken'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Instytucja', 'verbose_name_plural': 'Instytucje'},
        ),
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(to='charity_donation_app.category', verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='description',
            field=models.CharField(max_length=256, verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'Fundacja'), (2, 'Organizacja pozarządowa'), (3, 'Zbiórka lokalna')], default=1, verbose_name='Rodzaj instytucji'),
        ),
    ]