import os
import openrouteservice as ors
import folium
import secrets

from registration.models import Order
from collections import namedtuple
from tempfile import mkstemp
from pathlib import Path


path_to_templates = str(Path(__file__).resolve().parent.parent / 'templates/mapper')
Point = namedtuple('Point', ['x', 'y'])


def _parse_orders_json(orders: list[Order]) -> list[tuple]:
    coords = []
    for order in orders:
        jsn = order.places
        start = jsn['start'].split(',')
        end = jsn['end'].split(',')

        startpoint = Point(x=float(start[0]), y=float(start[1]))
        endpoint = Point(x=float(end[0]), y=float(end[1]))

        coords.append((startpoint, endpoint))

    return coords


def _create_map(coords: list[tuple], profile: str = 'driving-car'):
    client = ors.Client(key=os.getenv('KEY'))

    # по первой координате масштабируем карту
    folmap = folium.Map(location=[coords[0][0].y, coords[0][0].x], zoom_start=10)  # reverse -> [y,x]

    i = 1
    for coordinate in coords:
        try:
            routes = client.directions(coordinate, profile=profile, format='geojson')
        except:  # TODO: find ApiError from ors docs
            raise ValueError('direction not found')

        folium.GeoJson(routes, name=f'route{i}').add_to(folmap)

        folium.Marker(
            location=[coordinate[0].y, coordinate[0].x],
            popup=f'from {i}',
            icon=folium.Icon(color='blue')
        ).add_to(folmap)

        folium.Marker(
            location=[coordinate[1].y, coordinate[1].x],
            popup=f'to {i}',
            icon=folium.Icon(color='red')
        ).add_to(folmap)

        i += 1

    return _get_html_file_name_from_folium(folmap)


def _get_html_file_name_from_folium(folmap: folium.Map) -> str:
    """костыль, потому что не можем получить html напрямую"""
    filename = 'map_{0}.html'.format(secrets.token_hex(8))
    folmap.save('{0}/{1}'.format(path_to_templates, filename))

    return filename


def get_map_file_name(orders: list[Order]):
    coords = _parse_orders_json(orders)
    return _create_map(coords)
