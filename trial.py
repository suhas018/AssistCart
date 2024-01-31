from django.db import migrations
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path


DATA_FILENAME = 'C:/Users/DELL/Desktop/DESK/Projects/kart-pool/data/sample-data.json'
CITY = 'Visakhapatnam'

def load_data(apps, schema_editor):
    Store = apps.get_model('stores', 'Store')
    jsonfile = Path(__file__).parents[2] / DATA_FILENAME

    with open(str(jsonfile)) as datafile:
        try:
            objects = json.load(datafile)
            elements = objects.get('elements', [])

            for obj in elements:
                objType = obj.get('Type', '')
                if objType == 'node':
                    tags = obj.get('tags', {})
                    name = tags.get('name', 'N/A')

                    longitude = obj.get('lon', 0)
                    latitude = obj.get('lat', 0)
                    location = fromstr(f'POINT({latitude} {longitude})', srid=4326)

                    housenumber = tags.get('addr:housenumber', 'N/A')
                    street = tags.get('addr:street', 'N/A')
                    postcode = tags.get('addr:postcode', 'N/A')
                    address = housenumber + ',' + street + ',' + postcode

                    store_type = tags.get('shop', 'N/A')
                    phone = tags.get('phone', 'N/A')

                    Store(
                        name=name,
                        latitude=latitude,
                        longitude=longitude,
                        location=location,
                        store_type=store_type,
                        phone=phone[:100],
                        address=address[:100],
                        city=CITY,
                    ).save()
        except json.JSONDecodeError:
            pass