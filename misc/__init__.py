"""
some helper functions for python

"""

__author__ = 'coop'
__license__ = 'GPLv2'


import sys
import logging as log


def die(rc, message):
    """print message and exit

    Note: if no logger is configured, there is no output-message
        use the outcommented line instead

    Arguments:
    rc:         returncode
    message:    log message
    """
    log.error(message)
    #print(message)
    sys.exit(rc)


