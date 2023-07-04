from model.widespread.configuration import config_read


def corrector(dictionary):
    for type_convert in dictionary.items():
        try:
            dictionary[type_convert[0]] = int(type_convert[1])
        except ValueError:
            try:
                dictionary[type_convert[0]] = float(type_convert[1])
            except ValueError:
                dictionary[type_convert[0]] = str(type_convert[1])
    return dictionary


# Get the config parser object
FRAME_PARAMETERS = corrector(config_read(file_to_read='config.ini', special_section='frame_parameters'))
ALGORITHM_PARAMETERS = corrector(config_read(file_to_read='config.ini', special_section='algorithm_parameters'))
TRACKER_PARAMETERS = corrector(config_read(file_to_read='config.ini', special_section='tracker_parameters'))
CCTV_CONNECTION = corrector(config_read(file_to_read='config.ini', special_section='connection'))
