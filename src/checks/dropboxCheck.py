#!/usr/bin/env python
###############################################################################################
#  Author: 
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
_name = 'dropboxCheck'
# Descrip: 
_description = '''Check if there are errors or inconsistencies in dropbox'''
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
import glob
import shellutils

def check (properties):
    '''This procedure checks the whole dropbox tree looking for errors 
    and returns a list with suspicious file
    '''
    try:
        code, output, error = shellutils.run(["find", properties.get('dropboxCheck', 'dropboxpath')])
        return shellutils.grep("Case Conflict", output)
    
    except Exception as error:
        print "Error:", error
