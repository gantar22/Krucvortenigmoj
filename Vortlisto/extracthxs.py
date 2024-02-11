
vorataro = open("vortlisto.dict")
sheets = open("sheetsdoc.dict")

output = open("ĥ.dict","w")

for line in vorataro.readlines() + sheets.readlines():
    w = line.split(';')[0]
    if 'ĥ' in w:
        output.write(line.split(';')[0] + ';100\n')

output.close()
