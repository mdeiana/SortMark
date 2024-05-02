# SortMark
You've added a bookmark to Edge recently, but you can't remember how you organized it. You look for an option to sort all of your exessively many bookmakrs by date added, but you soon realize Microsoft for some reason hasn't implemented that feature.

##### This is what SortMark is for. **Also supports Chrome/Chromium bookmarks.**

## Usage
Print the last `n` bookmarks added in Edge with
```powershell
py SortMark.py -i n
```

Or do it for the last `n` **used** bookmarks with
```powershell
py SortMark.py -i n --lastUsed
```

Or do it for Chrome bookmarks (assumes default directory)
```powershell
py SortMark.py -i n --file chrome
```

Or for any Bookmarks file that follows the Chromium standard
```powershell
py SortMark.py -i n --file /path/to/file
```
Or write to file instead of printing to `stdout`, and write all the bookmarks by omitting the `-i` flag
```powershell
py SortMark.py -o sorted_bookmarks.txt
```

Of course, you can always refer to the help screen:
```
usage: SortMark [-h] [--added | --lastUsed] [--output OUTPUT] [--items N] [--file BOOKDIR]

Sort Chrome and Edge bookmarks by date added or date last used

options:
  -h, --help            show this help message and exit
  --added, -a
  --lastUsed, -l        Choose sorting strategy (default: by date added i.e. --added)
  --output OUTPUT, --out OUTPUT, -o OUTPUT
                        Choose file to print sorted bookmarks to (default: stdout)
  --items N, -i N, --count N, -c N, --number N, -n N
                        Specify how many items to print (default: all)
  --file BOOKDIR, -f BOOKDIR
                        Specify path to Bookmarks file (default: Chrome or Edge default on Windows), whichever is
                        found first. You may also specify "-f chrome" or "-f edge" to use default dir for specified
                        browser. Note that default dir is %USERPROFILE%\AppData\Local\<COMPANY>\<BROWSER>\User
                        Data\Default\Bookmarks
```