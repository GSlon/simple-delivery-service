from django.shortcuts import render
from django.http import HttpResponse
from .services.dbservice import get_orders_by_courier_id
from .services.mapapi import get_map_file_name
from .services.fsservice import prepare_dir
from pathlib import Path


path_to_templates = str(Path(__file__).resolve().parent / 'templates/mapper')


def default_path():
    return HttpResponse('id not found')


def get_map(request, id: int):
    orders = get_orders_by_courier_id(id)
    if len(orders) != 0:
        prepare_dir(path_to_templates)
        filename = get_map_file_name(orders)
        return render(request, 'mapper/' + filename)
    else:
        return HttpResponse('no orders found')
