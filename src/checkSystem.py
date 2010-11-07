#!/usr/bin/env python
###############################################################################################
#  Author: 
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
_name = 'checkSystem'
# Descrip: 
_description = '''Check if there are errors or inconsistencies in the current system'''
# Version: 
_version = '0.0.1'
#    Date:
_date = '20101107'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 
#          0.0.1 (20101107)
#            -Initial release
###############################################################################################

# Imports
import logging
import sys
import doctest
import datetime, time
import os
import subprocess
import optparse
import inspect
import ConfigParser
import glob
import imp

# Parameters, Globals n' Constants
callingDirectory = os.getcwd()
scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)
propertiesName = _name + ".properties"
propertiesPath = os.path.join(scriptDir, '..', propertiesName) 

# User-libs imports (This is the correct way to do this)
LIB_PATH = scriptDir + os.path.sep + '..' + os.path.sep + 'lib'
for infile in glob.glob(os.path.join(LIB_PATH, '*.*')):
    sys.path.insert(0, infile)
    
import shellutils
import generalutils

# Usage function, logs, utils and check input
def checkInput():
    '''This function is for treat the user command line parameters.
    '''

    #Create instance of OptionParser Module, included in Standard Library
    p = optparse.OptionParser(description=_description,
                              prog=_name,
                              version=_version,
                              usage='''%prog <eMail>''') 
    
    #Parse the commandline
    options, arguments = p.parse_args()

    #Decide what to do
    if len(arguments) != 1 :
        p.print_help()
        sys.exit(-1)
        
    else:
        return arguments
   
def readConfig():
    '''This procedure returns the program properties file
    '''
    config = ConfigParser.RawConfigParser()
    config.read(propertiesPath)
    return config
    
def saveConfig(config):
    '''This procedure returns the program properties file
    '''
    with open(propertiesPath, 'wb') as configfile:
        config.write(configfile)

# Main function
def main(email):
    '''This is the main procedure
    '''
    properties = readConfig()

    line = "0 * * * * " + scriptPath + " " + email  # Every hour
    if not generalutils.isInCron(line):
        generalutils.setCron(line)
       
    errors = {}

    try:    
        CHECKS_PATH = scriptDir + os.path.sep + 'checks'
        sys.path.insert(0, CHECKS_PATH)

        for name in shellutils.ls(CHECKS_PATH, type = "files"):
            if shellutils.extension(name) == 'py':
                (file, pathname, description) = imp.find_module(shellutils.filename(name))
                currentCheck = imp.load_module(shellutils.filename(name), file, pathname, description)
   
                currentCheckErrors = currentCheck.check(properties)
                
                if currentCheckErrors != None:
                    errors[shellutils.filename(name)] = currentCheckErrors
        
    except ImportError as error:
        print "Error:", error

    if len(errors) != 0:
        print errors
        
        gmail_user=properties.get('General', 'gmail_user')
        gmail_pwd=properties.get('General', 'gmail_pwd')
        generalutils.mail(gmail_user, gmail_pwd, email, _name + " report", str(errors))
        
    saveConfig(properties)
   
# Entry point
if __name__ == '__main__':
    parameters = checkInput()
    main(email=parameters[0])
