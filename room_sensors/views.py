# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from read_sensors import *

# Create your views here.

def homepage(request):
    temp_vals = TempReader.get_current()
    page_context = {'sensor_values': temp_vals}
    return render(request, 'room_sensors/homepage.html', page_context)

def api_sensor(request):
    temp_vals = TempReader.get_current()
    return JsonResponse(temp_vals)

def api_sensor_historical(request):
    temp_vals = TempReader.get_historical()
    return JsonResponse(temp_vals)
