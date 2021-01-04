lines = []
with open("..\VIS-group-C\dataset\sensor_data\BOS210.csv","r") as file:
    for line in file.readlines():
        if line[21] == "#":
            line = line.replace("#", ";#", 1)
        lines.append(line)


with open("..\VIS-group-C\dataset\sensor_data\BOS210_test.csv", "w") as f:
    for line in lines:
        f.write(line)
