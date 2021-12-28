import re

lines = []
with open("hi") as file_in:
    for line in file_in:
        if re.search(r"Discovered open port ", line) : 
            ipresult = re.search(r"(([0-9]+)(.)([0-9]+)(.)([0-9]+)(.)([0-9]+))", line)
            portresult = re.search(r"(([0-9]+)(/))", line)
            ip = ipresult.groups()[0]
            port = portresult.groups()[1]
            line=(ip+':'+port)
            lines.append(line)
        elif len(line)=='':
            r=0
            print('empty line')
        

with open('hi', 'w') as f:
    for item in lines:
        f.write("%s\n" % item)

