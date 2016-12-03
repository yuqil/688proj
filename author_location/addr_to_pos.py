import geocoder
import requests
file = open("author_address.txt")
output = open("author_latlng_yuqi2.txt", "wb")

print "start"
startline = 14616 + 2500
i = 0

for line in file:
    token = line.split("\t")
    name = token[0]
    addr = token[1]

    i += 1
    if i <= startline:
        continue
    try:
        g = geocoder.google(token[1])
        print i, g.latlng
        if len(g.latlng) == 2:
            output.write(name + "\t" + str(g.latlng[0]) + "\t" + str(g.latlng[1]) + "\n")
    except requests.exceptions.ReadTimeout:
        print "timeout"
        continue

file.close()
output.close()

