bitlibroj = open('artefaktoj/bitlibroj.dict')
bitlibroj = bitlibroj.readlines()
bitlibroj = [line.split(';')[0] for line in bitlibroj if ';' in line]

tekstaro = open('artefaktoj/tekstaro.dict')
tekstaro = tekstaro.readlines()
tekstaro = [line.split(';')[0] for line in tekstaro if ';' in line]
tekstaro = set(tekstaro)


output = []
for w in bitlibroj:
    if not w in tekstaro:
        output.append(w)

print(output)