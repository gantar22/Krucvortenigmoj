
file = open("artefaktoj/vortlisto.dict")
output = open("palindromoj.dict",'w')
for line in file.readlines():
    print(line)
    if len(line.split(';')[0]) > 1 and line.split(';')[0] == line.split(';')[0][::-1]:
        output.write(line.split(';')[0] + '\n')

output.close()
file.close()