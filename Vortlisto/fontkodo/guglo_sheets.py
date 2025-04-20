import itertools

outputfile = open("sheetsdoc.dict","w")

replacementsfile = open("./font_datumoj/guglo_sheets/replacement.csv")
lines = replacementsfile.readlines()
for line in lines:
    items = line.split(',')
    words = items[0].split()
    for word in words:
        outputfile.write(word + ';' + items[1] + '\n')


people = open("./font_datumoj/guglo_sheets/people.csv")
lines = people.readlines()
for line in lines:
    items = line.split(',')
    nameparts = items[0].split()
    for name in itertools.combinations(nameparts,len(nameparts)):
        outputfile.write(''.join(name) + ';70' + '\n')

music = open("./font_datumoj/guglo_sheets/music.csv")
lines = music.readlines()
lines = lines[2:]
for line in lines:
    items = line.split(',')
    nameparts = items[0].split()
    for name in itertools.combinations(nameparts,len(nameparts)):
        outputfile.write(''.join(name)  + ';' + str(max((items[1].lower() == "true") * 70, (items[2].lower() == "true") * 60, (items[3].lower() == "true") * 55)) + '\n')

expressions = open("./font_datumoj/guglo_sheets/expressions.csv")
lines = expressions.readlines()
lines = lines[1:]
for line in lines:
    items = line.split(',')
    if(len(items[0]) > 0):
        outputfile.write(''.join(items[0].split()) + ";60\n")


outputfile.close()
