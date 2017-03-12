import datetime
import io
import time

class Logger:
    def __init__(self, loglevel, logfile):
        self.logdebugmessages = loglevel == 'debug'
        self.logfile = logfile

    def __logtofile(self, msg):
        try:
            f = open(self.logfile,'a')
            f.write(str(msg) + '\n')
            f.close()
        except IOError:
            print 'IO error occured. Unable to write to log.'

    def info(self, msg):
        self.__logtofile(self.getPrefix('info') + str(msg))

    def debug(self, msg):
        if self.logdebugmessages:
           self.__logtofile(self.getPrefix('debug') + str(msg))

    def getPrefix(self, loglevel):
        timestamp = time.time()
        humanreadable = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return '%s [%s]: ' % (str(humanreadable), loglevel.upper())
