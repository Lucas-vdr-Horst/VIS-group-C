def fix_hashtags(filename):
    """ splits the hashtag that are attached to the datetime with ';', the seperator of the csv file"""
    new_filename = f"..\VIS-group-C\dataset\sensor_data\{'new_'+filename}"
    filename = f"..\VIS-group-C\dataset\sensor_data\{filename}"
    lines = []
    with open(filename,"r") as file:
        for line in file.readlines():
            if line[21] == "#":
                line = line.replace("#", ";#", 1)
            lines.append(line)


    with open(new_filename, "w") as f:
        for line in lines:
            f.write(line)

fix_hashtags("BOS210.csv")