import folium

from django.shortcuts import get_object_or_404, render

from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.photo:
            add_pokemon(
                folium_map,
                pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url)    
            )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.photo:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.photo.url,
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })  

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    requested_pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    requested_pokemon_entities = requested_pokemon.pokemon_entities.all()

    pokemon_with_entities = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'entities': [
            {
                'level': entity.level,
                'lat': entity.latitude,
                'lon': entity.longitude,
            } for entity in requested_pokemon_entities
        ]
    }
    if requested_pokemon.previous_evolution:
        pokemon_with_entities['previous_evolution'] = {
            'title_ru': requested_pokemon.previous_evolution.title,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(
                requested_pokemon.previous_evolution.photo.url)
        }
    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions:
        pokemon_with_entities['next_evolution'] = {
            'title_ru': next_evolutions[0].title,
            'pokemon_id': next_evolutions[0].id,
            'img_url': request.build_absolute_uri(next_evolutions[0].photo.url)
        }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    if not requested_pokemon.photo:
        return render(request, 'pokemon.html', context={
            'map': folium_map._repr_html_(), 'pokemon': pokemon_with_entities
        })
        
    pokemon_with_entities['img_url'] = request.build_absolute_uri(
        requested_pokemon.photo.url)
    for pokemon_entity in pokemon_with_entities['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon_with_entities['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_with_entities
    })
