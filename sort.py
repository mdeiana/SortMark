import re
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
        print(f"Bookmark {id}, found at line {self.line}:")
        print(f"\tName: {self.name}")
        print(f"\tUrl: {self.url}")
        print(f"\tDate added: {self.makeHuman(0).astimezone()}")
        print(f"\tDate last used: {self.makeHuman(1).astimezone()}")

    def makeHuman(self, sort_by: int) -> datetime:
        # Chromium timestamps are in microseconds since 1601-01-01
        if sort_by == 0:
            timestamp = self.date_add
        else:
            timestamp = self.date_lastU
        
        windows_epoch = datetime(1601, 1, 1)
        delta = timedelta(microseconds=timestamp)
        human_datetime = windows_epoch + delta
        return human_datetime

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
    # get sort_by
    sort_by = input("0 to sort by date_added, 1 by date_lastU: ")
    if sort_by == '0':
        sort_by = "--added"
    else:
        sort_by = "--lastUsed"

    

    # populate bookmarks list
    bookmarks = []
    i = 0

    with open("Bookmarks", "r") as f:
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
                sortInsert(bookmarks, bookmark, sort_by)

    print("Collection complete. Printing...\n")
    # print to file
    with open("out.txt", "w") as f:
        for i, bm in enumerate(bookmarks):
            f.write(f"Bookmark {i+1}, found at line {bm.line}:\n")
            f.write(f"\tName:\t\t {bm.name}\n")
            f.write(f"\tUrl:\t\t {bm.url}\n")
            f.write(f"\tDate added:\t {bm.makeHuman(0).strftime('%Y-%m-%d at %H:%M UTC')}\n")
            f.write(f"\tDate last used:\t {bm.makeHuman(1).strftime('%Y-%m-%d at %H:%M UTC')}\n")
            #f.write(f"Dates: {bm.date_add} {bm.date_lastU}\n\n")
            f.write('\n')
            









if __name__ == "__main__":
    main()