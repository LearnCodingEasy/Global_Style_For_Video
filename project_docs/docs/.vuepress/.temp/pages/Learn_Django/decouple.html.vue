<template><div><h1 id="decouple" tabindex="-1"><a class="header-anchor" href="#decouple"><span>Decouple</span></a></h1>
<div class="" dir="rtl">
<p>المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.</p>
</div>
<h2 id="website" tabindex="-1"><a class="header-anchor" href="#website"><span>Website</span></a></h2>
<p><a href="https://pypi.org/project/python-decouple/" target="_blank" rel="noopener noreferrer">Decouple</a></p>
<h2 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h2>
<div class="" dir="rtl">
1️⃣ ثبّت المكتبة
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip install python-decouple</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="create" tabindex="-1"><a class="header-anchor" href="#create"><span>Create</span></a></h2>
<div class="" dir="rtl">
2️⃣ أنشئ ملف .env في جذر المشروع
<p>في نفس مسار manage.py، أنشئ ملف جديد اسمه:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.env</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY<span class="token operator">=</span>django<span class="token operator">-</span>insecure<span class="token operator">-</span>sgt<span class="token operator">+</span>4e<span class="token comment">#-f%qpz%3p8jd9z4%)2b^8@+v40m!ws^j^t(l%m-io7x</span></span>
<span class="line">DEBUG<span class="token operator">=</span><span class="token boolean">True</span></span>
<span class="line">DB_NAME<span class="token operator">=</span>myprojectdb</span>
<span class="line">DB_USER<span class="token operator">=</span>myprojectuser</span>
<span class="line">DB_PASSWORD<span class="token operator">=</span>mypassword</span>
<span class="line">DB_HOST<span class="token operator">=</span>localhost</span>
<span class="line">DB_PORT<span class="token operator">=</span><span class="token number">5432</span></span>
<span class="line">GOOGLE_OAUTH_CLIENT_ID<span class="token operator">=</span><span class="token number">300012533519</span><span class="token operator">-</span>3buflbtimhmardd7t1ou7tc9qs6p6tks<span class="token punctuation">.</span>apps<span class="token punctuation">.</span>googleusercontent<span class="token punctuation">.</span>com</span>
<span class="line">GOOGLE_OAUTH_CLIENT_SECRET<span class="token operator">=</span>GOCSPX<span class="token operator">-</span>m3cGZDYkH581WK2_z0wJwmgZjuNu</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="edit" tabindex="-1"><a class="header-anchor" href="#edit"><span>Edit</span></a></h2>
<div class="" dir="rtl">
3️⃣ عدّل settings.py
<p>استورد المكتبة في بداية الملف:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="" dir="rtl">
وبدل القيم الثابتة بالمتغيرات:
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">'SECRET_KEY'</span><span class="token punctuation">)</span></span>
<span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">'DEBUG'</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> cast<span class="token operator">=</span><span class="token builtin">bool</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'GOOGLE_OAUTH_CLIENT_ID'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'GOOGLE_OAUTH_CLIENT_SECRET'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'SCOPE'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'profile'</span><span class="token punctuation">,</span> <span class="token string">'email'</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'AUTH_PARAMS'</span><span class="token punctuation">:</span> <span class="token punctuation">{</span><span class="token string">'access_type'</span><span class="token punctuation">:</span> <span class="token string">'online'</span><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'OAUTH_PKCE_ENABLED'</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">DATABASES <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">'default'</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'ENGINE'</span><span class="token punctuation">:</span> <span class="token string">'django.db.backends.postgresql'</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'DB_NAME'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'USER'</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'DB_USER'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'PASSWORD'</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'DB_PASSWORD'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'HOST'</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'DB_HOST'</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">'localhost'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'PORT'</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">'DB_PORT'</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">'5432'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="" dir="rtl">
4️⃣ تجاهل ملف .env
<p>عشان تحميه من الصعود للـ git, أضف .env إلى .gitignore:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.env</span>
<span class="line">*.env</span>
<span class="line">.env.local</span>
<span class="line">.env.production</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


