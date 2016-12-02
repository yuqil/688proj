import geocoder
import requests


g = geocoder.google('Mountain View, CA')
g.latlng

file = open("author_address.txt")
output = open("author_latlng.txt", "wb")

for line in file:
    token = line.split("\t")
    name = token[0]
    addr = token[1]
    try:
        g = geocoder.google(token[1])
        print g.latlng
        if len(g.latlng) == 2:
            output.write(name + "\t" + str(g.latlng[0]) + "\t" + str(g.latlng[1]) + "\n")
    except requests.exceptions.ReadTimeout:
        print "timeout"
        continue

file.close()
output.close()

