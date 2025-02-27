# Student Dormitory Maintenance Appointment System

1. เพื่อพัฒนาระบบแจ้งซ่อมบำรุงที่สามารถส่งคำขอซ่อมได้อย่างรวดเร็วและมีประสิทธิภาพ ลดความล่าช้าระหว่างนักศึกษาและผู้ดูแลหอพัก
2. เพื่อเพิ่มความสะดวกให้กับนักศึกษาในการแจ้งปัญหาการชำรุดของอุปกรณ์หรือสิ่งอำนวยความสะดวกในห้องพัก โดยสามารถระบุรายละเอียดได้อย่างครบถ้วน
3. เพื่อช่วยให้เจ้าของหอพักและช่างซ่อมสามารถติดตามและจัดลำดับความสำคัญของงานซ่อมบำรุงได้อย่างเป็นระบบ ลดความผิดพลาดในการรับข้อมูลและการดำเนินงาน
4. เพื่อเพิ่มประสิทธิภาพในการซ่อมบำรุง โดยช่วยให้ช่างซ่อมได้รับข้อมูลที่ถูกต้องเกี่ยวกับอาการเสีย อุปกรณ์ที่ต้องใช้ และตำแหน่งของห้องพักก่อนเข้าดำเนินการ
5. เพื่อช่วยลดความเสียหายที่อาจเกิดขึ้นเพิ่มเติมจากการซ่อมล่าช้า และทำให้สิ่งอำนวยความสะดวกภายในหอพักอยู่ในสภาพพร้อมใช้งานตลอดเวลา
6. เพื่อพัฒนาระบบติดตามสถานะงานซ่อม ทำให้นักศึกษาและผู้เกี่ยวข้องสามารถตรวจสอบความคืบหน้าของการซ่อมได้แบบเรียลไทม์
7. เพื่อปรับปรุงคุณภาพชีวิตของนักศึกษาให้ดีขึ้น โดยสร้างระบบที่ช่วยให้การอยู่อาศัยในหอพักมีความสะดวกสบายและมีประสิทธิภาพมากยิ่งขึ้น

# Pre Setup
- Python 3.x
- PostgreSQL
- pip
- Node.js
- npm

# Frontend Dependencies

ใน Next.js ที่ใช้
- axios
- bootstrap

# Backend Dependencies

# Setup Instructions
  ส่วนนี้คือการสอนการติดตั้งระบบ Student Dormitory Maintenance Appointment System (SDMAS) ตั้งแต่ต้นจนจบซึ่งอาจจะช่วยผู้ที่อยากจะใช้ระบบนี้สามารถนำไปปฏิบัติตามเพื่อให้ใช้ระบบนี้ได้อย่างถูกต้อง โดยจะแยกเป็นส่วยของภาษาอังกฤษ และส่วนของภาษาไทย

  This part is part of instruction for installation Student Dormitory Maintenance Appointment System (SDMAS). That teach how to install from scratch, So they can used this system correctly. There will be part for English and Thai.  

## Server Side (Django)

1. Check if <b>Python</b> is installed (เช็คว่า Python ถูกติดตั้งหรือยัง)
```
python --version
```
If not installed, Please Install [Python Download](https://www.python.org/downloads/)  

หากยังไม่ได้ติดตั้งให้ไปตามลิ้งค์นี้ [ติดตั้ง Python คลิ๊กตรงนี้!!!](https://www.python.org/downloads/)

2. Check if <b>pip</b> is installed (เช็คว่า pip ถูกติดตั้งหรือยัง)
```
pip --version
```
Or (หรือ)
```
python -m pip --version
```

If not installed, Please Install [pip Download](https://pip.pypa.io/en/stable/installation/)  

หากยังไม่ได้ติดตั้งให้ไปตามลิ้งค์นี้ [ติดตั้ง pip คลิ๊กตรงนี้!!!](https://pip.pypa.io/en/stable/installation/)  

3. Check if <b>Virtual Environment</b> is installed (เช็คว่า Virtual Environment ถูกติดตั้งหรือยัง)
```
python -m venv --help
```

If Virtual Environment is not installed, Please Install  
```
pip install virtualenv
```
หาก Virtual Environment ยังไม่ได้ติดตั้งให้ตามคำสั่งนี้
```
pip install virtualenv
```

4. Build Virtual Environment (สร้าง Virtual Environment)
```
python -m venv myvenv
```

5. Run Virtual Environment (เปิดใช้งาน Virtual Environment)
```
myvenv\Scripts\activate.bat
```

6. Check if <b>Django</b> is installed (เช็คว่า Django ถูกติดตั้งหรือยัง)  
```
django-admin --version
```
Or (หรือ)
```
python -m django --version
```

If Django is not installed, Please Install  
```
pip install django
```

หาก Django ยังไม่ได้ติดตั้งให้ตามคำสั่งนี้  
```
pip install django
```

7. Installed remaining dependencies
```
pip install humanize
pip install psycopg2
pip install psycopg2-binary
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
...
```
Or (หรือ)
If there was requirements.txt (หากมี requirements.txt)
```
cd SDMAS_django_nextjs
pip install -r requirements.txt
```

8. Migrate Database (ทำการ Migrate ฐานข้อมูล)
```
cd SDMAS_django_nextjs
python manage.py makemigrations
python manage.py migrate
```

9. Setting Database (ตั้งค่า Database)
```
# SDMAS_django_nextjs/SDMAS_django_nextjs/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SDMAS", # Database Name (ชื่อฐานข้อมูล)
        "USER": "postgres",  # Username (ชื่อผู้ใช้)
        "PASSWORD": "xxxxx",  # Password (รหัสผ่าน)
        "HOST": "localhost", # Hostname (ชื่อของโฮลส์)
        "PORT": "8000", # Port (พอร์ตที่ใช้)
    }
}
```

10. Run server (เปิดใช้งานเซิฟเวอร์)
```
cd SDMAS_django_nextjs
py manage.py runserver 8080
```

## Client Side (Next.JS)

1. Check if <b>Node JS</b> is installed (เช็คว่า Node JS ถูกติดตั้งหรือยัง)
```
node -v
```
Or (หรือ)
```
node --version
```
If Node JS is not installed, Please Install [Download Node JS Here](https://nodejs.org/en/download)
หาก Node JS ยังไม่ได้ติดตั้งให้ [ดาวน์โหลด Node JS ตรงนี้](https://nodejs.org/en/download)

2. Check if <b>npm</b> is installed (เช็คว่า npm ถูกติดตั้งหรือยัง)
* Basically npm will be installed with Node JS by default, So this step just check that npm is installed correctly. (โดยทั่วไปแล้ว nom จะถูกติดตั้งมาพร้อมกับ Node JS อยู่แล้ว ขั้นตอนนี้ก็เป็นเพียงการเช็คว่า npm ถูกติดตั้งแล้วหรือยัง)
```
npm -v
```

If npm is not installed, Please Install
```
npm install -g npm
```

หาก npm ยังไม่ได้ติดตั้งให้ 
```
npm install -g npm
```
  
หากต้องการใช้ Node Package Manager ตัวอื่นก็สามารถใช้ได้ เช่น pnpm
```
npm install -g pnpm
```

3. Install Dependencies (ติดตั้ง package ที่จำเป็น)
```
cd django-nextjs-frontend
npm install
```

4. Run Server (การเปิดใช้งานเซิฟเวอร์)
```
npm run build
npm start
```
