import xml.etree.ElementTree as ET

def open_xml(file_name):
    """
    Returns a xml out of the given directory.
    
    :param file_name: the name of the xml put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    :type str

    :returns: an xml readable in python
    :type xml.Element
    """

    tree = ET.parse("intersections/{}".format(file_name))
    root = tree.getroot()
    print(type(root))
    return root


def get_lane_length(file_name):
    """
    Dictionary with length of every lane.

    :param file_name: the name of the xml put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    :type str

    :returns: an dictionary with all length of a lane by laneID
    :type dict
    """
    xml_file = open_xml(file_name)


if __name__ == "__main__":
    get_lane_length('BOS210/79190154_BOS210_ITF_COMPLETE.xml')
    