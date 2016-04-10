from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import *
from .serializers import LocationSerializer
from .utils import calculate_route_wrapper

from django.http import JsonResponse

from mongoengine import *

connect("travel")


def map(request):
    return render(request, 'location/map.html')

##########################################################################################
# Location


def create_location(request):
    if request.method == 'POST':
        location_name = request.POST.get('name')
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')
        address = request.POST.get('address')
        placeId = request.POST.get('placeId')
        new_location = Location(name=location_name,
                                latitude=latitude,
                                longitude=longitude,
                                address=address).save()
        return new_location


def create_place(request):
    if request.method == 'POST':
        try:
            user = request.user
            alias = request.POST.get('alias')
            placeId = request.POST.get('placeId')
            description = request.POST.get('description')

            new_place = Place(alias=alias, description=description, owner=user)
            corresponding_location = Location.objects(placeId=placeId)
            if not corresponding_location:
                corresponding_location = create_location(request)
            new_place.location = corresponding_location

            new_place.save()
            return JsonResponse({"result":"Create new place successful."})
        except:
            return JsonResponse({"error":"Create new place failed."})


def load_places(request):
    bound = request.bound                   # TODO
    user = request.user
    locations = Location.objects(latlng__get_within_box=bound)
    return JsonResponse({"result": locations})


def location(request, location_id):
    return render(request, 'main.html', {'id':location_id})


class LocationList(generics.ListCreateAPIView):

    def get(self, request, format=None):
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = LocationSerializer(data=request.data, context={'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

##########################################################################################
# Route


def create_route(request):
    if request.method == 'POST':
        route_name = request.POST.get('name')
        require_auto_route = request.POST.get('auto')
        children_ids = request.POST.get('children_ids') # list

        locations = Place.objects(id__in=children_ids).only('location')
        points = Location.objects(id__in=location_ids).only('latlng')

        new_route = Route(name=route_name)
        new_route.children = Place.objects(location__id__in=children_ids)
        if require_auto_route:
            geo_tree = calculate_route_wrapper(points)
            new_route.path = geo_tree
        new_route.save()


def load_route(request):
    route_id = request.route_id
    route = Route._object(_id=route_id)
    return JsonResponse(route)