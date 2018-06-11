from functools import reduce
from operator import or_

from django.db.models import Q

from django.shortcuts import render
from django.template.backends import django

from mobile.models import Mobile, Bands


def home(request):
    mobiles = Mobile.objects.all()
    template = 'base.html'
    return render(request, template, context={'mobiles': mobiles})


def queries(request, price=None, os=None, data=None, core=None):
    mobiles = Mobile.objects.all()
    filters = []
    if price != "all":
        prar = price.split('&')
        for ran in prar:
            chota, bada = ran.split('to')
            filters.append(">"+chota+" & <"+bada)
        condition = reduce(or_, [Q(price__range=(ran.split('to')[0], ran.split('to')[1])) for ran in prar])
        mobiles = mobiles.filter(condition)

    if os != "all":
        osar = os.split('&')
        for q in osar:
            filters.append(q)
        condition = reduce(or_, [Q(os__name__icontains=q) for q in osar])
        mobiles = mobiles.filter(condition)

    if data != "all":
        bnar = data.split('&')
        for band in bnar:
            mobiles = mobiles.filter(band__name=band)
            filters.append(band)

    if core != "all":
        mobiles = mobiles.filter(proccessor_speed__range=(0.0, core))
        filters.append("Less than " + core + " GHz")

    template = 'base.html'
    return render(request, template, context={'mobiles': mobiles,
                                              'core': core,
                                              'filters': filters})


def search(request, query=None):
    q = Q(brand__name__icontains=query) | Q(model__icontains=query) | Q(os__name__icontains=query) | Q(name__icontains=query) | Q(price__icontains=query) | Q(proccessor_speed__icontains=query)
    mobiles = Mobile.objects.filter(q)
    template = 'base.html'
    return render(request, template, context={'mobiles': mobiles})