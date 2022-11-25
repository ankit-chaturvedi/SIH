import geocoder
def loc():
    g = geocoder.ip('me')
    return g.latlng

print(loc())
