
roots_file = open("./Vortlisto/artefaktoj/roots.txt")

roots = set()

for line in roots_file.readlines():
    for w in line.split():
        roots.add(w)


for w in roots:
    
