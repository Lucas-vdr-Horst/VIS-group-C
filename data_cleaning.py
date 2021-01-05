import os


def fix_hashtags(filename):
    """ splits the hashtag that are attached to the datetime with ';', the seperator of the csv file"""
    new_filename = os.path.join("dataset", "sensor_data",f"new_{filename}")
    filename = os.path.join("dataset", "sensor_data", filename)
    lines = []
    with open(filename,"r") as file:
        for line in file.readlines():
            if line[21] == "#":
                line = line.replace("#", ";#", 1)
            lines.append(line)

    with open(new_filename, "w") as f:
        for line in lines:
            f.write(line)


if __name__ == "__main__":
    fix_hashtags("BOS210.csv")