from django.db import models 


class Pokemon(models.Model):
    title = models.CharField('Имя покемона на русском', max_length=50)
    photo = models.ImageField('Изображение', upload_to='images', blank=True)
    description = models.TextField('Описание', blank=True,
        default='описание скоро появится')
    title_en = models.CharField('Имя на английском', max_length=50, default='-')
    title_jp = models.CharField('Имя на японском', max_length=50, default='-')
    previous_evolution = models.ForeignKey('self', blank=True, null=True,
        on_delete=models.SET_NULL, related_name='next_evolutions',
        verbose_name='Из кого эволюционирует')

    def __str__(self):
        return f'Покемон {self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
        verbose_name='Тип покемона')
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления', null=True)
    disappeared_at = models.DateTimeField('Время исчезновения', null=True)
    level = models.IntegerField('Уровень', default=0)
    health = models.IntegerField('Здоровье', default=0)
    strength = models.IntegerField('Атака', default=0)
    defence = models.IntegerField('Защита', default=0)
    stamina = models.IntegerField('Выносливость', default=0)

    def __str__(self):
        return f'{self.pokemon.title} Lev. {self.level}'
