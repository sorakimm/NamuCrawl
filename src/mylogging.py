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
        except Exception as reason:
            pass
        try:
            fileHd = logging.FileHandler(filename)
            fileHd.setLevel(logging.ERROR)
            fileHd.setFormatter(fmtHandler)
            self.addHandler(fileHd)
        except Exception as reason:
            self.error("%s" % reason)

        try:
            rtfHandler = logging.handlers.BaseRotatingHandler(
                filename, maxBytes=10 * 1024 * 1024, backupCount=5)
        except Exception as reason:
            self.error("%s" % reason)
        else:
            self.addHandler(rtfHandler)

        return



