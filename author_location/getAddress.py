

file = open("/Users/yuqil/Desktop/16fall/15688/final project/code/688proj/base_dir/original-data/AMiner-Author.txt")

dict = {}

cur_name = None
cur_address = None
read_name = False

for line in file:
    if line.startswith("#n"):
        cur_name = line.rstrip()[3:]
        read_name = True
    elif line.startswith("#a"):
        if read_name:
            cur_address = line.rstrip()[3:]
            dict[cur_name] = cur_address
        read_name = False
        cur_name, cur_address = None, None
    else:
        continue



person = open("/Users/yuqil/Desktop/16fall/15688/final project/code/688proj/base_dir/new_person.txt")
output = open("author_address.txt", "wb")
for line in person:
    line = line.rstrip()
    name = line[line.find(",") + 1 :]
    if name in dict:
        addr = dict[name]
        if len(addr) > 0:
            if ";" in addr:
                addr = addr[0 : addr.find(";")]
            output.write(name + "\t" + addr + "\n")
            print name, addr

output.close()
person.close()

