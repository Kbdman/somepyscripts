#!/usr/bin/python3
from pathlib import Path
import os.path
import shutil
import sys


def MoveContentTo(cur, dest):
    print("In " + str(cur))
    p = Path(cur)
    if not p.exists():
        return
    InRoot=False
    if str(cur)==dest:
        InRoot=True
    for x in p.iterdir():
        fileabxpath = str(x)
        if x.is_dir() and x.name != "." and x.name != '..':
            MoveContentTo(x, dest)
            shutil.rmtree(fileabxpath)
        elif x.is_file() and not InRoot:
            move = True
            if os.path.exists(dest + "/" + x.name):
                if os.path.getsize(dest + "/" + x.name) >= os.path.getsize(fileabxpath):
                    print("内层文件小，不移动"+x.name)
                    move = False
                else:
                    os.remove(dest + "/" + x.name)
            if move:
                print("移动" + shutil.move(fileabxpath, dest))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("cmd error")
    else:
        r=sys.argv[1]
        MoveContentTo(Path(r),r)