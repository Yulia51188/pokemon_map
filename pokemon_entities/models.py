from django.db import models 


class Pokemon(models.Model):
    title = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images', blank=True)
    
    def __str__(self):
        return f'Покемон {self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField('уровень', default=0)
    health = models.IntegerField('здоровье', default=0)
    strength = models.IntegerField('атака', default=0)
    defence = models.IntegerField('защита', default=0)
    stamina = models.IntegerField('выносливость', default=0)

    def __str__(self):
        return f'{self.pokemon.title} Lev. {self.level}'
