import zipfile
import sys
import os

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("usage: zipcracker.py <zipfile> <password list> [num threads]")
    sys.exit(1)

filename = sys.argv[1]
pwlist = sys.argv[2]
thr = 4
try:
    if len(sys.argv) == 4:
        thr = int(sys.argv[3])
except:
    print("error: incorrect number of threads")
    sys.exit(4)

if not os.path.exists(filename):
    print(f"error: zip file {filename} doesn't exist")
    sys.exit(2)

if not os.path.exists(pwlist):
    print(f"error: password list file {pwlist} doesn't exist")
    sys.exit(3)

def try_deflate(password):
    try:
        with zipfile.ZipFile(filename) as zfile:
            zfile.extractall(pwd=password.encode('utf-8'))
        return True
    except:
        return False

if __name__ == '__main__':
    with open(pwlist, 'r') as pwfile:
        for password in pwfile:
            password = password.strip()  # Loại bỏ ký tự newline
            print(f"Trying password: {password}")
            if try_deflate(password):
                print(f"Password found: {password}")
                break
        else:
            print("Password not found.")
