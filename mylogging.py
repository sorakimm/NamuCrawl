# -*- coding:utf-8 -*-
import os
import logging
import logging.handlers


class MyLogger(logging.Logger):
    def __init__(self, filename='log/test.log'):
        logging.Logger.__init__(self, filename)

        fmtHandler = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s():%(lineno)s][%(levelname)s] %(message)s')

        try:
            consoleHd = logging.StreamHandler()
            consoleHd.setLevel(logging.INFO)
            consoleHd.setFormatter(fmtHandler)
            self.addHandler(consoleHd)
        except Exception as reason:
            self.error("%s" % reason)


        try:
            os.makedirs(os.path.dirname(filename))
        except Exception as e:
            pass
        try:
            rtfileHd = logging.handlers.RotatingFileHandler(filename, maxBytes=10 * 1-24 * 1024, backupCount=5)
            rtfileHd.setLevel(logging.INFO)
            rtfileHd.setFormatter(fmtHandler)
            self.addHandler(rtfileHd)
        except Exception as reason:
            self.error("%s" % reason)

        return



