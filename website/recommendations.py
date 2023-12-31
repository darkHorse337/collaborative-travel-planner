import googlemaps
import requests
from geopy.geocoders import Nominatim
import spacy
from .secret import GOOGLE_API_KEY

map = googlemaps.Client(GOOGLE_API_KEY)
geolocator = Nominatim(user_agent="place-locator")

def text_processor(user_input):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)

    needed_adjectives = [
        'american', 'italian', 'mexican', 'french', 'chinese', 'japanese', 'indian', 'thai', 'greek', 'mediterranean',
        'spanish', 'korean', 'vietnamese', 'middle eastern', 'moroccan', 'turkish', 'lebanese', 'german', 'english',
        'irish', 'african', 'ethiopian', 'nigerian', 'south african', 'caribbean', 'jamaican', 'cuban',
        'latin american',
        'brazilian', 'peruvian', 'argentinian', 'colombian', 'australian', 'indonesian', 'malaysian', 'filipino',
        'russian', 'scandinavian', 'swedish', 'norwegian', 'danish', 'polish', 'turkish', 'mexican', 'spanish',
        'arabic', 'israeli', 'georgian', 'pakistani', 'afghan', 'persian', 'iraqi', 'kurdish', 'austrian', 'swiss',
        'belgian', 'portuguese', 'czech', 'hungarian', 'dutch', 'surinamese', 'sri lankan', 'tibetan', 'nepali',
        'mongolian',
        'cambodian', 'laotian', 'maldivian', 'bangladeshi', 'bhutanese', 'hawaiian', 'alaskan', 'polynesian',
        'micronesian',
        'caribbean', 'cuban', 'puerto rican', 'jamaican', 'trinidadian', 'haitian', 'dominican', 'bahamian',
        'caymanian',
        'central american', 'mexican', 'guatemalan', 'salvadoran', 'honduran', 'nicaraguan'
    ]

    filtered_tokens = []

    noun_added = False
    adjective_added = False

    try:
        for token in doc:
            if token.pos == 'NOUN' and token.text.lower() and not noun_added:
                filtered_tokens.append(token.text.lower())
                noun_added = True
            elif token.pos == 'ADJ' and not adjective_added:
                filtered_tokens.append(token.text.lower())
                adjective_added = True
    except:
        pass

    try:
        for token in doc:
            if token.text.lower() in needed_adjectives:
                filtered_tokens.append(token.text.lower())
    except:
        pass

    try:
       if output != None:
            output = ' '.join(filtered_tokens)
       else:
            output = user_input
    except:
        output = user_input
    return output
def find_locations(location, radius=1000, keyword=None, types=None):
    location_coordinates = geolocator.geocode(location)
    try:
        if location_coordinates:
            places_result = map.places_nearby(
                location=(location_coordinates.latitude, location_coordinates.longitude),
                radius=radius,
                open_now=False,
                keyword=keyword,
                type=types
            )

            places = places_result.get('results', [])
            return places
        else:
            print("Can't find coordinates the location")
            return []
    except:
        location_coordinates = geolocator.geocode('NYC')
        places_result = map.places_nearby(
            location=(location_coordinates.latitude, location_coordinates.longitude),
            radius=radius,
            open_now=False,
            keyword='hotels',
            type=types
        )
def get_location_details(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={GOOGLE_API_KEY}'

    response = requests.get(url)
    data = response.json()

    if 'result' in data:
        rating = data['result'].get('rating', 'N/A')
        photos = data['result'].get('photos', [])
        
        photo_url = ''
        if photos:
            photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photos[0]["photo_reference"]}&key={GOOGLE_API_KEY}'

        return rating, photo_url
    else:
        return 'N/A', ''

def recommend_locations(user_city, distance_filter, keyword):

    recommended_places_with_ratings = []

    places = find_locations(user_city, radius=distance_filter, keyword=keyword, types=keyword)

    for place in places[0:5]:
        place_id = place.get('place_id')
        if place_id:
            rating, photo_url = get_location_details(place_id)
            recommended_places_with_ratings.append({
                'name': place['name'],
                'address': place['vicinity'],
                'rating': rating,
                'photo_url': photo_url
            })

    sorted_places = sorted(recommended_places_with_ratings, key=lambda x: float(x['rating']) if x['rating'] != 'N/A' else -1, reverse=True)

    return sorted_places

def run_algorithm(user_city, query):
    recommended_places = recommend_locations(user_city=user_city, distance_filter=5000, keyword=query)
    return recommended_places