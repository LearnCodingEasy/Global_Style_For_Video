<template><div><h1 id="postgresql" tabindex="-1"><a class="header-anchor" href="#postgresql"><span>PostgreSQL</span></a></h1>
<h2 id="installing-postgresql" tabindex="-1"><a class="header-anchor" href="#installing-postgresql"><span>Installing PostgreSQL</span></a></h2>
<p><a href="https://www.postgresql.org/download/" target="_blank" rel="noopener noreferrer">Download PostgreSQL</a></p>
<h2 id="install-psycopg2" tabindex="-1"><a class="header-anchor" href="#install-psycopg2"><span>Install psycopg2</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install psycopg2-binary</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install psycopg2</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="تشغيل-postgresql-على-windows" tabindex="-1"><a class="header-anchor" href="#تشغيل-postgresql-على-windows"><span>تشغيل PostgreSQL على Windows</span></a></h2>
<div class=" " style=" " dir="rtl">
<ol>
<li>استخدام SQL Shell (psql)</li>
</ol>
<p>بعد تثبيت PostgreSQL على Windows، هيكون عندك برنامج اسمه SQL Shell (psql).</p>
<p>افتحه من قائمة Start → اكتب &quot;SQL Shell&quot; واضغط Enter.</p>
</div>
<div class=" " style=" " dir="rtl">
<ol start="2">
<li>تسجيل الدخول</li>
</ol>
<p>اضغط Enter لكل القيم الافتراضية إلا عند كلمة المرور، هنا تدخل كلمة المرور اللي اخترتها أثناء تثبيت PostgreSQL.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Server [localhost]: (اضغط Enter)</span>
<span class="line">Database [postgres]: (اضغط Enter)</span>
<span class="line">Port [5432]: (اضغط Enter)</span>
<span class="line">Username [postgres]: (اضغط Enter)</span>
<span class="line">Password for user postgres: ********  ← هنا اكتب كلمة المرور</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  بعد إدخال كلمة المرور صح، هتشوف سطر الأوامر يتحول لـ:
<p>ده معناه أنك دخلت بنجاح، وممكن تبدأ تنفذ أوامر SQL.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">postgres=#</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  3. إنشاء قاعدة بيانات ومستخدم
<p>داخل postgres=# نفذ الأوامر دي:</p>
</div>
<div class=" " style=" " dir="rtl">
<p>1️⃣  إنشاء قاعدة بيانات جديدة باسم myprojectdb</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">CREATE DATABASE myprojectdb;</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
2️⃣  إنشاء مستخدم جديد في PostgreSQL باسم myprojectuser مع كلمة مرور mypassword
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">CREATE USER myprojectuser WITH PASSWORD 'mypassword';</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  3️⃣ تعيين الترميز (encoding) الافتراضي للمستخدم myprojectuser ليكون UTF-8.
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ALTER ROLE myprojectuser SET client_encoding TO 'utf8';</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  4️⃣  "read committed" يعني أن أي استعلام يقرأ بيانات موجودة فقط إذا تم تأكيدها بالفعل، لتجنب قراءة بيانات غير مكتملة.
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  5️⃣ الغرض: تعيين المنطقة الزمنية (timezone) الافتراضية للمستخدم myprojectuser.
<p>لماذا: لتوحيد الوقت في كل المعاملات، خصوصًا لو التطبيق يمكن استخدامه عالميًا.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ALTER ROLE myprojectuser SET timezone TO 'UTC';</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  6️⃣ منح جميع الصلاحيات للمستخدم على قاعدة البيانات myprojectdb.
<p>الصلاحيات تشمل: إنشاء الجداول، تعديل البيانات، حذف البيانات، إجراء استعلامات</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myprojectuser;</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class=" " style=" " dir="rtl">
  4. الخروج من SQL Shell
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">\q</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


