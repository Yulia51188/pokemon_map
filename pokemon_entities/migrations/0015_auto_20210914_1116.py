# Generated by Django 3.1.13 on 2021-09-14 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20210914_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemons', to='pokemon_entities.pokemon', verbose_name='Тип покемона'),
        ),
    ]
