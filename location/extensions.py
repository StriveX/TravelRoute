from .models import *

connect("travel")

def import_seed():
    l1 = Location(name="My Apartment", latlng=(37.795125, -122.430378), address="2000 Broadway St. San Francisco").save()
    l2 = Location(name="Zenefits", latlng=[37.785233, -122.395693], address="303 Second St. San Francisco").save()
    l3 = Location(name="Golden gate bridge", latlng=[37.8199295, -122.478255], address="San Francisco, CA").save()
    l4 = Location(name="WCRI", latlng=[43.474521, -80.537389], address="268 Phillip St. Waterloo ON. Canada").save()

    p1 = Place(alias="Home", location=l1, description="This is my SF home").save()
    p2 = Place(alias="Work", location=l2, description="My company").save()
    p3 = Place(alias="Canada home", location=l4, description="This is my Canada home").save()

