from configparser import ConfigParser
from model.joint.static_paths import path, STATIC_PATH

# Get the configparser object
config_object = ConfigParser()
config_object.read(path.join(STATIC_PATH, 'config.ini'))


def config_read(file_to_read, special_section):
    section_object = ConfigParser()
    section_object.read(path.join(STATIC_PATH, file_to_read))
    return dict(section_object[special_section])


def config_write():
    config_object["frame_parameters"] = {
        "FRAME_RED": "200",
        "FRAME_GREEN": "0",
        "FRAME_BLUE": "0",
        "FRAME_BGR": "(FRAME_BLUE, FRAME_GREEN, FRAME_RED)",
        "FRAME_RGB": "(FRAME_RED, FRAME_GREEN, FRAME_BLUE)",
        "THICKNESS": "1",
        "FRAME_SIZE": "400"
    }

    config_object["algorithm_parameters"] = {
        "SCALE_FACTOR": "1.1",  # different object size can be determined correctly with this value
        "MIN_NEIGHBORS": "6",  # look for pixel neighbors to determine correct object in algorithm
        "DIRECTION_SENSITIVITY": "3",  # used for detecting direction between frames (in pixel)
        "DIRECTION_FRAME_SENSITIVITY": "5",  # get direction between two specific frame
        "CONTOURS_THRESHOLD": "230",  # Used for thermal threshold.
        # optimizing the accuracy of algorithm: between 0.0 and 1

        "CONFIDENCE_THRESHOLD": "0.5",
        "CONFIDENCE_NMS_THRESHOLD": "0.6",
        # accuracy to performance ratio: fast: 1 - balanced: 2 - accuracy: 3
        "ACCURACY_PERFORMANCE_RATIO": "3",

        "WINDOWS_SIZE": "416"  # define windows size for dnn network
    }

    config_object["tracker_parameters"] = {
        # TRACKER_TYPES = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        "TRACKER_TYPE": "CSRT"
    }
    # Write the above sections to config.ini file
    with open('../../static/config.ini', 'w') as conf:
        config_object.write(conf)


def config_update(file, section, field, value):
    section_object = ConfigParser()
    section = section_object['{section}'.format(section)]
    section['{field}'.format(field)] = '{value}'.format(value)
    # Write changes back to file
    with open('{file}'.format(file), 'w') as conf:
        section_object.write(conf)
