"""
Some filesystem helper functions (UNIX) for python

    Written by DerCoop <dercoop@users.sourceforge.net>

"""

__author__ = 'coop'
__license__ = 'GPLv2'

import subprocess

def mount(partition, target, fs=None, options=None):
    """mount a partition

    Arguments:
    partition:  the partition to mount
    target:     the target where the partition should be mounted
    fs:         the filesystem of the partition to mount (optional)
    options:    the options (rw, ro ...) (optional)

    Return:
    The returncode of the mount command
    """
    cmd = ['mount', '-o', 'ro']
    if fs:
        cmd.extend(['-t', fs])
    if options:
        cmd.extend(['-o', options])
    cmd.append(partition)
    cmd.append(target)
    return subprocess.check_call(cmd)


def umount(target):
    """unmount a partition

    Arguments:
    target: the target to unmount

    Return:
    The returncode of the mount command
    """
    cmd = ['umount', target]
    return subprocess.check_call(cmd)

