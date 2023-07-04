import logging
from model.joint.static_paths import path, LOGS_PATH


class Logger:
    def __init__(self, logger_name):
        """personal logger which is built to handle default logs which is not working for mine"""
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages

        fh = logging.FileHandler(path.join(LOGS_PATH, '{name}.log'.format(name=logger_name)))
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    @staticmethod
    def __convert_tuple(message_in_tuple):
        string = ' '.join(map(str, message_in_tuple))
        return string

    def debug(self, *message):
        self.logger.debug(self.__convert_tuple(message))

    def info(self, *message):
        self.logger.info(self.__convert_tuple(message))

    def warning(self, *message):
        self.logger.warning(self.__convert_tuple(message))

    def error(self, *message):
        self.logger.error(self.__convert_tuple(message))

    def critical(self, *message):
        self.logger.critical(self.__convert_tuple(message))


if __name__ == '__main__':
    my_log = Logger('test')
    my_log.info('hi')