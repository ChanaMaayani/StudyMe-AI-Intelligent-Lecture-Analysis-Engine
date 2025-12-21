import requests
import os

# הכתובת של התעודה
url = "http://netfree.link/netfree-ca.crt"
print(f"Trying to download certificate from {url}...")

# הורדה ללא בדיקת אבטחה (כי עדיין אין לנו תעודה)
response = requests.get(url, verify=False)

# שמירת הקובץ בתיקייה הנוכחית
with open("netfree-ca.crt", "wb") as f:
    f.write(response.content)

print("✅ Success! The file 'netfree-ca.crt' is now in your folder.")