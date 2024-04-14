

file = open("vortlisto.dict")
output = open("triliteraj.dict",'w')
for line in file.readlines():
    print(line)
    if len(line.split(';')[0]) == 3:
        output.write(line.split(';')[0] + '\n')

output.close()
file.close()
