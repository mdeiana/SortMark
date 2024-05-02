import re
import os
import sys
import datetime
import argparse
from datetime import datetime, timedelta

class Bookmark:
    def __init__(self, date_add, date_lastU, name, url, line):
        self.date_add = date_add
        self.date_lastU = date_lastU
        self.name = name
        self.url = url
        self.line = line
    
    def printBook(self, id):
        print(f"Bookmark {id+1}, found at line {self.line}:")
        print(f"\tName:\t\t {self.name}")
        print(f"\tUrl:\t\t {self.url}")
        print(f"\tDate added:\t {self.makeHuman('--date_add')}")
        print(f"\tDate last used:\t {self.makeHuman('--date_lastUsed')}")
        print('\n')

    def writeBook(self, id, fstream):
        fstream.write(f"Bookmark {id+1}, found at line {self.line}:\n")
        fstream.write(f"\tName:\t\t {self.name}\n")
        fstream.write(f"\tUrl:\t\t {self.url}\n")
        fstream.write(f"\tDate added:\t {self.makeHuman('--date_add')}\n")
        fstream.write(f"\tDate last used:\t {self.makeHuman('--date_lastUsed')}\n")
        fstream.write('\n')

    def makeHuman(self, which_date) -> str:
        # Chromium timestamps are in microseconds since 1601-01-01
        if which_date == '--lastUsed':
            timestamp = self.date_lastU
        else:
            timestamp = self.date_add
        
        windows_epoch = datetime(1601, 1, 1)
        delta = timedelta(microseconds=timestamp)
        human_datetime = windows_epoch + delta
        return human_datetime.strftime('%Y-%m-%d at %H:%M UTC')

def sortInsert(bookmarks: list, bm: Bookmark, sort_by: str):
    #print(f"Len of passed bookmarks: {len(bookmarks)}")
    index = len(bookmarks)
    if sort_by == '--lastUsed':
        for i, bookmark in enumerate(bookmarks):
            if bm.date_lastU >= bookmark.date_add:
                index = i
                break
    else:
        for i, bookmark in enumerate(bookmarks):
            if bm.date_add >= bookmark.date_add:
                index = i
                break
    bookmarks.insert(index, bm)

def isolateNum(string):
    numbers = re.findall(r'\d+', string)
    if numbers:
        return int(numbers[0])
    return None

def isolateUrl(string: str) -> str:
    words = string.split()
    word = words[1][1:-1]
    return word

def isolateName(string: str) -> str:
    name = string[9:-2]
    return name

def main():
    # default Bookmarks paths in Windows, only used if another path isn't specified
    def_edgeBookDir = os.path.expandvars(r'%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks')
    def_chromeBookDir = os.path.expandvars(r'%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Bookmarks')
    info_defDir = r'%%USERPROFILE%%\AppData\Local\<COMPANY>\<BROWSER>\User Data\Default\Bookmarks'

    # parse arguments
    parser = argparse.ArgumentParser(
                prog="SortMark",
                description="Sort Chrome and Edge bookmarks by date added or date last used",
                epilog='Microsoft pls fix')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--added', '-a', dest='sort_by', default='--added', action="store_const", const='--added')
    group.add_argument('--lastUsed', '-l', dest='sort_by', default='--added', action='store_const', const='--lastUsed',
                        help='Choose sorting strategy (default: by date added i.e. --added)')
    
    parser.add_argument('--output', '--out', '-o', dest='output', default=None,
                        help="Choose file to print sorted bookmarks to (default: stdout)")
    parser.add_argument('--items', '-i', '--count', '-c', '--number', '-n',
                        dest='items', default=0, metavar='N', type=int,
                        help='Specify how many items to print (default: all)')
    parser.add_argument('--file', '-f', dest='bookDir', default=None,
                        help=f'Specify path to Bookmarks file (default: Chrome or Edge default on Windows),\
                         whichever is found first. You may also specify "-f chrome" or "-f edge"\
                         to use default dir for specified browser. Note that default dir is {info_defDir}')
    args = parser.parse_args()

    # if no arguments are provided, print help
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)


    # get right Bookmarks directory
    if not args.bookDir:
        if os.path.isfile(def_chromeBookDir):
            path = def_chromeBookDir
        elif os.path.isfile(def_edgeBookDir):
            path = def_edgeBookDir
    else:
        if args.bookDir.upper() == 'chrome'.upper():
            path = def_chromeBookDir
        elif args.bookDir.upper() == 'edge'.upper():
            path = def_edgeBookDir
        elif os.path.isfile(args.bookDir):
            path = args.bookDir
        else:
            print("SortMark: fatal: Provided directory is not valid")
            sys.exit()

    # populate bookmarks list
    bookmarks = []
    i = 0
    with open(path, "r") as f:
        while True:
            i += 1
            line = f.readline().strip()
            if line == '' or line.startswith('"sync_metadata":'):
                break
            elif line.startswith('"date_added":'):
                date_add = isolateNum(line)
            elif line.startswith('"date_last_used":'):
                date_lastU = isolateNum(line)
            elif line.startswith('"name":'):
                name = isolateName(line)
            elif line.startswith('"url":'):
                url = isolateUrl(line)
                bookmark = Bookmark(date_add, date_lastU, name, url, i)
                sortInsert(bookmarks, bookmark, args.sort_by)

    print("Collection complete. Printing...\n")

    # get right amount of items to print
    if args.items:
        upp_limit = enumerate(bookmarks[:args.items])
    else:
        upp_limit = enumerate(bookmarks)

    # print to file
    if args.output:
        with open(args.output, "w") as f:
            for i, bm in upp_limit:
                bm.writeBook(i, f)
    # print to stdout
    else:
        for i, bm in upp_limit:
            bm.printBook(i)










if __name__ == "__main__":
    main()