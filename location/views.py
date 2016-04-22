from json import loads
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import *
from .serializers import LocationSerializer
from .utils import calculate_route_wrapper

from mongoengine import *

connect("travel")


def index(request):
    user = request.user
    context = {'user': user}
    return render(request, 'location/map.html', context)


def dashboard(request):
    user = request.user
    context = {'user': user}
    return render(request, 'location/dashboard.html', context)

##########################################################################################
# Location


def create_location(request):
    if request.method == 'POST':
        user = request.user
        location_name = request.POST.get('name')
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')
        address = request.POST.get('address')
        placeId = request.POST.get('placeId')
        latlng = (float(latitude), float(longitude))
        print location_name, latitude, longitude, address
        new_location = Location(name=location_name,
                                latlng=latlng,
                                address=address,
                                placeId=placeId).save()
        return new_location


def create_place(request):
    if request.method == 'POST':
        try:
            # user = request.user
            alias = request.POST.get('alias')
            place_id = request.POST.get('placeId')
            description = request.POST.get('description')
            print alias, place_id, description
            new_place = Place(alias=alias, description=description)
            corresponding_location = Location.objects(placeId=place_id)
            if not corresponding_location:
                corresponding_location = create_location(request)
            new_place.location = corresponding_location
            new_place.save()
            return JsonResponse({"latlng": corresponding_location.latlng, "place_id": str(new_place.id)})
        except Exception as e:
            print e.args, e
            return JsonResponse({"error": "Create new place failed."})


def load_places(request):
    if request.method == 'GET':
        try:
            n = request.GET['n']
            e = request.GET['e']
            s = request.GET['s']
            w = request.GET['w']
            ne = (float(n), float(e)); sw = (float(s), float(w))
            # user = request.user
            locations = Location.objects(latlng__within_box=[sw, ne]).to_json()
            return JsonResponse(loads(locations), safe=False)
        except Exception as e:
            print e
            return JsonResponse({"error": e}, safe=False)


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

        locations = Place.objects(id__in=children_ids).only('id', 'location')

        new_route = Route(name=route_name)
        new_route.children = Place.objects(location__id__in=children_ids)
        if require_auto_route:
            geo_tree = calculate_route_wrapper(locations)
            new_route.path = geo_tree
        new_route.save()


def load_route(request):
    route_id = request.route_id
    route = Route._object(_id=route_id)
    return JsonResponse(route)