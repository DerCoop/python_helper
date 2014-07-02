"""
some helper functions for python

    Written by DerCoop <dercoop@users.sourceforge.net>

"""

__author__ = 'coop'
__license__ = 'GPLv2'


import sys
import logging as log


def die(rc, message):
    """print message and exit

    Note: This function uses the logging packet, if this is not configured
        use "print(message)" instead

    Arguments:
    rc:         returncode
    message:    log message
    """
    log.error(message)
    #print(message)
    sys.exit(rc)


def grep(fname, regex):
    """implementation of unix grep

    args:
    fname:  the name of the file which will be scanned
    regex:  the regular expression of the searchstring

    return:
    all matching lines

    """
    import re

    result = ''
    try:
        with open(fname) as fd:
            for line in fd:
                if re.search(regex, line):
                    if not line == None:
                        result = result + line
        return result
    except:
        raise


def add_files_to_tar(src_dir, archive_fd):
    """add all files from the src_dir and all subdirectories to an archive

    args:
    src_dir:    the directory with the source files (subdirectories are allowed)
    archive_fd: the file descriptor of the archive

    return:
    0:  on success
    1:  on failure

    """
    import os

    try:
        for f in os.listdir(src_dir):
            f = os.path.join(src_dir, f)
            if os.path.isdir(f):
                add_files_to_tar(f, archive_fd)
            else:
                archive_fd.add(f.lstrip('./'))
        return 0
    except:
        return 1


def tar_gz_dir(root_dir, archive):
    """add all files from the root_dir and all subdirectories to the gzipped archive

    args:
    root_dir:   the directory with the source files (subdirectories are allowed)
    archive:    the absolut path of the archive

    Note: if you use a relative path,
        make sure that the archive is not a part of the root directory!!

    Note: if the archive exists, it will be overwritten

    return:
    0:  on success
    1:  on failure

    """
    import os
    import tarfile

    cwd = os.getcwd()
    os.chdir(root_dir)
    with tarfile.open(archive, 'w:gz') as archive_fd:
        ret = add_files_to_tar('.', archive_fd)
    os.chdir(cwd)
    return ret


def copy_file(src_file, destination):
    """copy a file

    args:
    src_file:       the source file to copy
    destination:    the destination file (if it is a directory,
                    the filename is the same like the source file)

    return:
    0:  on success
    e:  on error

    """
    import shutil

    try:
        shutil.copy2(src_file, destination)
    except OSError, e:
        return e
    return 0


def copy_tree(srcdir, dstdir):
    """copy all files and dirs

    args:
    src_dir:    the source directory (subdirectories are allowed)
    dst_dir:    the destination directory, if it do not exists,
                it will be created

    """
    import os

    files = os.listdir(srcdir)
    if not os.path.exists(dstdir):
        os.mkdir(dstdir)
    for filename in files:
        srcfile = os.path.join(srcdir, filename)
        if not os.path.isdir(os.path.join(dstdir, filename)) \
                and not os.path.isdir(srcfile):
            copy_file(srcfile, dstdir)
        else:
            copy_tree(srcfile, os.path.join(dstdir, filename))


def cat(filename):
    """implementation of unix cat

    print content of a file to stdout

    args:
    filename:   the name of the file to print

    return:
    0:  on success
    1:  on error

    """
    import sys

    try:
        with open(filename, 'r') as fd:
            # read line by line, fast and memory efficient
            for line in fd:
                # print w/o leading newline
                sys.stdout.write(line)
    except:
        sys.stderr.write('Can\'t read file: %s\n', str(filename))
        return 1
    return 0


def get_md5sum_dir(directory):
    """get the md5 sum of a directory

    With this implementation, The MD5SUM of all (sums all files) is created
        each subdirectory will be added as md5sum

    args:
    directory:  the name of the directory to create a MD5SUM

    return:
    the MD5SUM of the directory

    """
    import hashlib
    import os

    md5sum = hashlib.md5()
    for files in os.listdir(directory):
        filename = os.path.join(directory, files)
        if os.path.isdir(filename):
            md5sum.update(get_md5sum_dir(filename))
        else:
            md5sum.update(get_md5sum(filename))
    return md5sum.hexdigest()


def get_md5sum(fqn):
    """get the md5sum of a file

    args:
    fqn:    the name of the file (with path)

    return:
    the MD5SUM of the file

    """
    import hashlib

    with open(fqn, 'rb') as fd:
        md5sum = hashlib.md5()
        while True:
            # if the file is to big, we must read small blocks
            data = fd.read(8192)
            if not data:
                break
            md5sum.update(data)
        return md5sum.hexdigest()


def get_yaml_value(dictionary, key, default=''):
    """returns the value of the key

    args:
    dictionary: the dict where the key is stored
    key:        the name of the key to get
    default:    the default value to return,
                    if the key not exists (by default '')

    return:
    key:        on success
    default:    if key not exists

    """
    if key in dictionary:
        return str(dictionary[key])
    else:
        return default


def read_config_file(filename):
    """read a bash config file and write the key value pairs to a dict

    filesyntax:
        # i am a comment
        key=value

    args:
    filename:   the name of the file to read

    return:
    dictionary: the dictionary with the read key - value pairs
    1:          on error

    """
    import sys

    dictionary = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # ignore empty lines and comments
                if line and not line[0] == '#':
                    split_line = line.split('=')
                    if len(split_line) == 2:
                        # <key>="<value>"
                        # we do not need quotes in python!
                        # Delete them all and add them at output, if required
                        dictionary.update(dict({split_line[0]: split_line[1].replace('\"', '')}))
    except:
        sys.stderr.write('Can\'t read file: %s\n', str(filename))
        return 1
    return dictionary
