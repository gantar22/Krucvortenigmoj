def main():
    l = open('tekstaro.count','r',encoding='utf8')
    output = open('tekstaro.dict','w',encoding='utf8')
    lines = l.readlines()
    for line in lines:
        output.write(f'{line.split('->')[0]};51\n')
    output.close()


main()