# PostgreSQL

## Installing PostgreSQL

[Download PostgreSQL](https://www.postgresql.org/download/)

## Install psycopg2

```cmd
pip install psycopg2-binary
```

```cmd
pip install psycopg2
```

## تشغيل PostgreSQL على Windows

<div class=" " style=" " dir="rtl">

1. استخدام SQL Shell (psql)

بعد تثبيت PostgreSQL على Windows، هيكون عندك برنامج اسمه SQL Shell (psql).

افتحه من قائمة Start → اكتب "SQL Shell" واضغط Enter.

</div>

<div class=" " style=" " dir="rtl">
  
  2. تسجيل الدخول

اضغط Enter لكل القيم الافتراضية إلا عند كلمة المرور، هنا تدخل كلمة المرور اللي اخترتها أثناء تثبيت PostgreSQL.

</div>

```
Server [localhost]: (اضغط Enter)
Database [postgres]: (اضغط Enter)
Port [5432]: (اضغط Enter)
Username [postgres]: (اضغط Enter)
Password for user postgres: ********  ← هنا اكتب كلمة المرور
```

<div class=" " style=" " dir="rtl">
  بعد إدخال كلمة المرور صح، هتشوف سطر الأوامر يتحول لـ:

ده معناه أنك دخلت بنجاح، وممكن تبدأ تنفذ أوامر SQL.

</div>

```
postgres=#
```

<div class=" " style=" " dir="rtl">
  3. إنشاء قاعدة بيانات ومستخدم

داخل postgres=# نفذ الأوامر دي:

</div>

<div class=" " style=" " dir="rtl">
  
1️⃣  إنشاء قاعدة بيانات جديدة باسم myprojectdb
</div>

```
CREATE DATABASE myprojectdb;

```

<div class=" " style=" " dir="rtl">
2️⃣  إنشاء مستخدم جديد في PostgreSQL باسم myprojectuser مع كلمة مرور mypassword
</div>

```
CREATE USER myprojectuser WITH PASSWORD 'mypassword';

```

<div class=" " style=" " dir="rtl">
  3️⃣ تعيين الترميز (encoding) الافتراضي للمستخدم myprojectuser ليكون UTF-8.
</div>

```
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';

```

<div class=" " style=" " dir="rtl">
  4️⃣  "read committed" يعني أن أي استعلام يقرأ بيانات موجودة فقط إذا تم تأكيدها بالفعل، لتجنب قراءة بيانات غير مكتملة.
</div>

```
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';

```

<div class=" " style=" " dir="rtl">
  5️⃣ الغرض: تعيين المنطقة الزمنية (timezone) الافتراضية للمستخدم myprojectuser.

لماذا: لتوحيد الوقت في كل المعاملات، خصوصًا لو التطبيق يمكن استخدامه عالميًا.

</div>

```
ALTER ROLE myprojectuser SET timezone TO 'UTC';

```

<div class=" " style=" " dir="rtl">
  6️⃣ منح جميع الصلاحيات للمستخدم على قاعدة البيانات myprojectdb.

الصلاحيات تشمل: إنشاء الجداول، تعديل البيانات، حذف البيانات، إجراء استعلامات

</div>

```
GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myprojectuser;

```

<div class=" " style=" " dir="rtl">
  4. الخروج من SQL Shell
</div>

```
\q

```
