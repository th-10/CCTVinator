import sys
city = sys.argv[1]


def get_weather(place):  
    return place**2

print(get_weather(city))
sys.stdout.flush()