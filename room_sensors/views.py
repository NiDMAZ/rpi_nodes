# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from read_sensors import *

# Create your views here.

def homepage(request):
    temp_vals = TempReader.get_current()
    page_context = {'sensor_values': temp_vals}
    return render(request, 'room_sensors/homepage.html', page_context)
