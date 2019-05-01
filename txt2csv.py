INPUT_FILE = "maze5.txt"

OUTPUT_FILE = "maze5.csv"

with open(INPUT_FILE) as f:
    data = f.readlines()

newdata = []

for line in data:
    ln = []
    for c in line.strip():
        ln.append(c)
    newdata.append(ln.copy())

with open(OUTPUT_FILE, "w") as f:
    for ln in newdata:
        line = ""
        for c in str(ln):
            try:
                line += str(int(c))
                line += ","
            except:
                pass
        fline = ""
        for i in range(len(line) - 1):
            fline += line[i]
        fline += "\n"
        f.write(fline)
