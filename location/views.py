from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Location
from .serializers import LocationSerializer

def map(request):
    return render(request, 'location/map.html')

def load_locations(request):
    locations = Location.objects.all()

@login_required
def add_location(request):
    if request.method == 'POST':
        location_name = request.POST.get('name')
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lng')
        address = request.POST.get('address')
        description = request.POST.get('description')
        print request.POST, latitude, longitude

        location = Location(name=location_name,
                            latitude=latitude,
                            longitude=longitude,
                            address=address,
                            description=description)
        location.save()

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