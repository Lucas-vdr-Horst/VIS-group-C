import os
import shutil


def fix_hashtags(intersection_name, filename):
    """ splits the hashtag that are attached to the datetime with ';', the seperator of the csv file"""
    new_filename = os.path.join("dataset", intersection_name, f"new_{filename}")
    old_filename = os.path.join("dataset", intersection_name, filename)
    lines = []
    with open(old_filename, "r") as file:
        for line in file.readlines():
            if line[21] == "#":
                line = line.replace("#", ";#", 1)
            lines.append(line)

    with open(new_filename, "w") as f:
        for line in lines:
            f.write(line)
    shutil.move(old_filename, os.path.join("dataset", "Original", filename))


if __name__ == "__main__":
    fix_hashtags("BOS210", "BOS210.csv")
