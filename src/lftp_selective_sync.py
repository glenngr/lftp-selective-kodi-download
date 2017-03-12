'''
Created on 28. mar. 2015

@author: GGreibesland
'''
from subprocess import Popen, PIPE, STDOUT
import sys
import shutil
import os
from config import *
from imdb import getImdbID, getImdbRating
from log import Logger as SimpleLogger
from xbmc import xbmcHasMovie

logger = SimpleLogger('debug' if debug else 'info', logfile)

if not remoteUser or not remoteHost or not remotePass:
    remote = '-u %s,%s %s' % (sys.argv[0], sys.argv[1], sys.argv[2])
else:
    remote = '-u %s,%s %s' % (remoteUser, remotePass, remoteHost)


class lftpcommand:
    def __init__(self, remoteLogin, remotePath):
        self.commandList = []
        self.lftp_logfile = os.getcwd() + '/output.log'
        self.lftpsettings = 'set xfer:eta-period 5;set xfer:log true\,set xfer:log-file %s;set xfer:rate-period 20;' % (self.lftp_logfile)
        self.cmdpre = 'open %s;cd %s;' % (remoteLogin, remotePath)
        self.cmdpre += self.lftpsettings
        self.cmdpost = ''

    def add(self, command):
        self.commandList.append(command)
        
    def get(self):
        return self.cmdpre + ';'.join(self.commandList) + self.cmdpost
    
    def clear(self):
        self.commandList = []

    def getLogFile(self):
        return self.lftp_logfile


def runLftp(lftpcmd, watch=False):
    lrun = ['lftp', '-c', lftpcmd.get()]
    process = Popen(lrun, stdout=PIPE)
    if watch:
        logf = lftpcmd.getLogFile()
        while process.poll() is None:
            print file(logf, "r").readlines()[-1]
            time.sleep(2)
    return Popen(lrun, stdout=PIPE).communicate()[0]


def downloadRemoteNfos(remote=remote,remotepath=remotepath):
    cleanTemp()
    commands = lftpcommand(remote, remotepath)
    getnfoscommand = 'mirror -i ./*.nfo'
    if only_folders_newer_than:
        try:
            maxage = int(only_folders_newer_than)
            # Only get files with creating date between now and maxage days ago.
            getnfoscommand += ' --newer-than=now-%sdays' % str(maxage)
            logger.info('Valid only_folders_newer_than setting found. Only getting nfo files newer than %d days' % maxage)
        except ValueError:
            err = 'Invalid value in "only_folders_newer_than" setting'
            print(err)
            logger.info(err)
    commands.add('lcd temp')        
    commands.add(getnfoscommand)
    runLftp(commands)


def getMoviesToFetch(nfos):
# Now we have a replicated directory structure with only the nfo files.
# Loop through nfo files, find imdb id
    mirrordirs = []
    for nfo in nfos:
        if nfo != '':
            dir = '/'.join(nfo.split('/')[:-1])
            file = nfo[-1]
            imdb = getImdbID(nfo)
	    if not imdb:
	        logger.info('No imdb id found in ' + nfo)
            else:
                logger.debug('NFO File: ' + nfo + ', imdb id: ' + imdb)
            xbmc = xbmcHasMovie(imdb, mysqlHost, mysqlLogin, mysqlPassword, mysqlDatabase)
            if imdb and not xbmc:
                if requireMinimumImdbRating:
		    rating = getImdbRating(imdb)
 		else:
		    rating = 99.0
		if rating >= minimumImdbRating or rating <= lowerImdbRating:
                    mirrordirs.append(dir.replace('temp/', ''))
		elif rating < minimumImdbRating:
                    logger.info("Movie is not within the required rating score " + imdb + " with " + str(rating))
		
    return mirrordirs


def fetchMovies(directories):
    commands = lftpcommand(remote, remotepath)
    commands.add('lcd "%s"' % (localpath))
    commands.add('pwd')
    for d in directories:
       commands.add('mirror -c -P%i "%s"' % (lftp_parallell, d))
    commands.add('quit')
    # Download
    logger.debug('Running with commands: ' + commands.get())
    runLftp(commands)


def cleanTemp():
    tempdir = os.getcwd() + '/temp'
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

def getLocalNfoFiles():
    nfos = []
    for root, dirs, files in os.walk('./temp'):
        for file in files:
            if file.endswith('.nfo'):
                nfos.append(os.path.join(root, file))
    return nfos


def run_selective_sync():
    downloadRemoteNfos()
    nfoFiles = getLocalNfoFiles()
    logger.debug('NFO Files: ')
    logger.debug(nfoFiles)
    downMovies = getMoviesToFetch(nfoFiles)
    logger.debug('Folders to download:')
    logger.debug(downMovies)
    fetchMovies(downMovies)


if __name__ == "__main__":
    run_selective_sync()

