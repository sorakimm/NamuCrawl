# -*- coding:utf-8 -*-

import logging

#
# class MyLogger(logging.Logger):
#
#     def __init__(self, filename='log/test.log', level=logging.DEBUG):
#         logging.Logger.__init__(self, filename)
#         # self.logger = logging.getLogger(name)
#         self.logger.setLevel(level)
#
#         file_handler = logging.FileHandler('%s.log' % filename, 'w')
#         self.logger.addHandler(file_handler)
#
#         stream_handler = logging.StreamHandler()
#         stream_Formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s][%(levelname)s] %(message)s')
#         # stream_Formatter = logging.Formatter('%(asctime)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s')
#
#         stream_handler.setFormatter(stream_Formatter)
#         self.logger.addHandler(stream_handler)
#
#     # def debug(self, msg):
#     #     self.logger.debug(msg)
#     #
#     # def info(self, msg):
#     #     self.logger.info(msg)
#     #
#     # def warning(self, msg):
#     #     self.logger.warning(msg)
#     #
#     # def error(self, msg):
#     #     self.logger.error(msg)

# # if __name__ == '__main__':
# #     # log = MyLogger()
# #     # log.debug('debug')
# #     # log.info('info')
# #     # log.warning('warning')
# #     # log.error('error')
# #     mylogger = MyLogger()
# #     mylogger.debug('debug')
#
#


# coding:cp949
import os
import logging


class MyLogger(logging.Logger):
    def __init__(self, filename='test.log'):
        logging.Logger.__init__(self, filename)

        fmtHandler = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s():%(lineno)s][%(levelname)s] %(message)s')

        try:
            consoleHd = logging.StreamHandler()
            consoleHd.setLevel(logging.ERROR)
            consoleHd.setFormatter(fmtHandler)
            self.addHandler(consoleHd)
        except Exception as reason:
            self.error("%s" % reason)

        try:
            os.makedirs(os.path.dirname('log/%s.log' % filename))
        except Exception as reason:
            pass
        try:
            fileHd = logging.FileHandler('log/%s.log' % filename, 'w')
            fileHd.setLevel(logging.ERROR)
            fileHd.setFormatter(fmtHandler)
            self.addHandler(fileHd)
        except Exception as reason:
            self.error("%s" % reason)

        return


