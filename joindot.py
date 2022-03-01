#!/usr/bin/python3.7
#
# joindot - Combine multiple graphviz .dot format files
#
# - Input: Multiple .dot files
#   - It is assumed that there is one `digraph`
# - Output: A .dot file
#   - Generate a `digraph` with multiple `subgraph`s
#
import os
import sys
import argparse
import glob
import shutil

__version__ = '0.0.1'

# V: Verbose message
V=False
#V=True

def ECHO(msg):
    print(msg, flush=True)

def VERBOSE(msg):
    global V
    if not V == False:
        print(msg, flush=True)

def CMD(cmd, msg):
    echo_msg = cmd if not V == False else msg
    ECHO(echo_msg)
    os.system(cmd)

def CP(src, dst):
    VERBOSE('CP     ' + src + ' ' + dst)
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        pass

def MV(src, dst):
    VERBOSE('MV     ' + src + ' ' + dst)
    try:
        shutil.move(src, dst)
    except shutil.FileNotFoundError:
        pass
    except shutil.SameFileError:
        pass

def MKDIR(path):
    if not path:
        print('Error: MV required an argument pathname.')
        sys.exit(1)
    if not os.path.exists(DST_DIR):
        try:
            VERBOSE('MKDIR  ' + path)
            os.makedirs(DST_DIR)
        except:
            print('Error: cannot create directory "{0}"'.format(path))
            sys.exit(1)

def PWD():
    return os.getcwd()

def CD(path=None):
#   if not path:
#       print('Error: CD required an argument pathname.')
#       sys.exit(1)
    cwd = os.getcwd()
    if path:
        try:
            VERBOSE('CD     ' + path)
            # print('Current working directory: {0}'.format(os.getcwd()))
            os.chdir(path)
            # print('Working directory changed to: {0}'.format(os.getcwd()))
        except:
            print('Error: cannot change directory to "{0}"'.format(path))
            sys.exit(1)
    return cwd

def boolean_string(s):
    if s not in {'False', 'True', 'false', 'true', 'FALSE', 'TRUE'}:
        raise ValueError('Not a valid boolean string')
    return (s == 'True') or (s == 'true') or (s == 'TRUE')

def add_prefix(dirs, pfx):
    l = []
    for x in dirs:
        l.append(pfx + x)
    return l

def chext(path, ext):
    return os.path.splitext(path)[0] + ext

def getext(path):
    return os.path.splitext(path)[1]

def get_dir_files_by_ext(dir, ext):
    l = []
    for f in os.listdir(dir):
        if getext(f) == ext:
            l.append(dir + f)
            #print('dir = ' + dir + ' file = ' + f)
    return l

def get_source_files(dirs):
    l = []
    for dir in dirs:
        for f in os.listdir(dir):
            if f[-2:] == '.c':
                l.append(dir + f)
    return l


CWD = PWD()
SRC_DIR = None
SRC_FILES = []
DST_DIR = None
DST_FILE = 'joined.dot'
DST_PATH = None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '-D', required=False, action='store', dest='cwd', type=str, default=None
            , help='Change to DIR before performing any operations.')
    parser.add_argument('-V', required=False, dest='V', type=boolean_string, default=False
            , help='Verbose message')
    parser.add_argument('-I', '--src_dir', dest='src_dir', required=False, action='store', type=str, default=None
            , help='[in] Directory pathname, which contains .dot files.')
    parser.add_argument('--src_files', dest='src_files', action='store', type=str, nargs='*', default=[]
            , help='[in] Input .dot file list.')
    parser.add_argument('-O', '--dst_dir', dest='dst_dir', required=False, action='store', type=str, default=None
            , help='[out] Destination directory path.')
    parser.add_argument('-o', '--dst_file', dest='dst_file', required=False, action='store', type=str, default=None
            , help='[out] Destination .dot file path.')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()

    # Process argument variables
    global V
    V = args.V
    if args.cwd:
        CD(args.cwd)
    if args.src_dir:
        global SRC_DIR
        SRC_DIR = args.src_dir
    if args.dst_dir:
        global DST_DIR
        DST_DIR = args.dst_dir
    if args.dst_file:
        global DST_FILE
        DST_FILE = args.dst_file

    if (not args.dst_file) and (SRC_DIR):
        dirname = os.path.basename(os.path.abspath(SRC_DIR))
        if dirname:
            DST_FILE = dirname + '.dot'
            VERBOSE("DST_FILE = {0}".format(DST_FILE))

    if DST_DIR:
        MKDIR(DST_DIR)
        DST_PATH = DST_DIR + os.path.sep + os.path.basename(DST_FILE)
    else:
        DST_PATH = DST_FILE

    if SRC_DIR:
        # SRC_FILES = get_dir_files_by_ext(SRC_DIR + os.path.sep, '.dot')
        SRC_FILES.extend( glob.glob(SRC_DIR + os.path.sep + "*.dot") )

    SRC_FILES.extend( args.src_files )

    if not V == False:
        VERBOSE("SRC_FILES:")
        for f in SRC_FILES:
            VERBOSE("{0}".format(f))
        VERBOSE("DST_PATH: {0}".format(DST_PATH))

    #
    # join each .dot files, and save to DST_PATH.
    #
    for f in SRC_FILES:
        in_file = f
        fname = os.path.basename(in_file)
        VERBOSE("in_file = {0}".format(in_file))
        # VERBOSE("fname = {0}".format(fname))

        with open(DST_PATH, 'w') as outfile:
            outfile.write('digraph "' + os.path.basename(DST_PATH) + '" {\n')
            outfile.write('rankdir = "TB"\n')
            outfile.write('overlap=false\n')
            for in_path in SRC_FILES:
                with open(in_path) as infile:
                    for line in infile:
                        # Replace 'digraph' to 'subgraph'.
                        line = line.replace('digraph "', 'subgraph "cluster', 1)
                        outfile.write(line)
            outfile.write('}\n')

if __name__ == '__main__':
    main()
