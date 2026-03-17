<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<h3 id="_1️⃣-install" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install"><span>1️⃣ Install</span></a></h3>
<h4 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django-allauth</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 4️⃣ django-allauth</span></span>
<span class="line">ACCOUNT_LOGOUT_ON_GET <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> <span class="token string">"300012533519-3buflbtimhmardd7t1ou7tc9qs6p6tks.apps.googleusercontent.com"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> <span class="token string">"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"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line">"none" ➝ من غير تحقق.</span>
<span class="line">"optional" ➝ التحقق اختياري.</span>
<span class="line">"mandatory" ➝ لازم يتحقق عشان الحساب يتفعل ✅.</span>
<span class="line">"""</span></span>
<span class="line">ACCOUNT_EMAIL_VERIFICATION <span class="token operator">=</span> <span class="token string">'optional'</span></span>
<span class="line">ACCOUNT_USER_MODEL_USERNAME_FIELD <span class="token operator">=</span> <span class="token boolean">None</span></span>
<span class="line">ACCOUNT_SIGNUP_FIELDS <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"email"</span><span class="token punctuation">,</span> <span class="token string">"name"</span><span class="token punctuation">,</span> <span class="token punctuation">]</span></span>
<span class="line">ACCOUNT_LOGIN_METHODS <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token string">"email"</span><span class="token punctuation">}</span></span>
<span class="line">LOGIN_REDIRECT_URL <span class="token operator">=</span> <span class="token string">"http://127.0.0.1:8000"</span></span>
<span class="line">LOGOUT_REDIRECT_URL <span class="token operator">=</span> <span class="token string">"/accounts/login/"</span></span>
<span class="line">EMAIL_BACKEND <span class="token operator">=</span> <span class="token string">'django.core.mail.backends.console.EmailBackend'</span></span>
<span class="line">SITE_ID <span class="token operator">=</span> <span class="token number">1</span></span>
<span class="line">SOCIALACCOUNT_AUTO_SIGNUP <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">ACCOUNT_UNIQUE_EMAIL <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">ACCOUNT_EMAIL_REQUIRED <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">SOCIALACCOUNT_ADAPTER <span class="token operator">=</span> <span class="token string">"users_accounts.adapter.MySocialAccountAdapter"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Libraries</span></span>
<span class="line">  <span class="token string">'django.contrib.sites'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'allauth'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'allauth.account'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'allauth.socialaccount'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'allauth.socialaccount.providers.google'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">MIDDLEWARE <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Add AccountMiddleware for allauth</span></span>
<span class="line">  <span class="token string">"allauth.account.middleware.AccountMiddleware"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 📄 [ backend_django/urls.py ] ملف</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path<span class="token punctuation">,</span> include</span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"accounts/"</span><span class="token punctuation">,</span> include<span class="token punctuation">(</span><span class="token string">"allauth.urls"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


