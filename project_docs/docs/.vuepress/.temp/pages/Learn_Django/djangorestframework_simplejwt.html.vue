<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<h3 id="_1️⃣-install" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install"><span>1️⃣ Install</span></a></h3>
<h4 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework-simplejwt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<div dir="rtl" style="font-size:1vw">
<ul>
<li>
<p>ACCESS_TOKEN_LIFETIME: مدة صلاحية توكن الوصول (Access token) لمدة 30 يوم.</p>
</li>
<li>
<p>REFRESH_TOKEN_LIFETIME: مدة صلاحية توكن التحديث (Refresh token) لمدة 180 يوم.</p>
</li>
<li>
<p>ROTATE_REFRESH_TOKENS: لو True، كل مرة تستخدم فيها refresh token يتم إبطال القديم وإصدار جديد، هنا معطّل.</p>
</li>
</ul>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> datetime <span class="token keyword">import</span> timedelta</span>
<span class="line"></span>
<span class="line">SIMPLE_JWT <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"ACCESS_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"REFRESH_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">180</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"ROTATE_REFRESH_TOKENS"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Django REST Framework settings for identity and permissions verification</span></span>
<span class="line"><span class="token comment"># Use JWT for identity verification</span></span>
<span class="line"><span class="token comment"># Allow only authenticated users</span></span>
<span class="line">REST_FRAMEWORK <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"DEFAULT_AUTHENTICATION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"rest_framework_simplejwt.authentication.JWTAuthentication"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"DEFAULT_PERMISSION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span><span class="token string">"rest_framework.permissions.IsAuthenticated"</span><span class="token punctuation">,</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Libraries</span></span>
<span class="line">  <span class="token string">"rest_framework_simplejwt"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="_3️⃣-used" tabindex="-1"><a class="header-anchor" href="#_3️⃣-used"><span>3️⃣ used</span></a></h3>
<div dir="rtl" style="font-size:1.5vw">
  تحديث حالة المستخدم فى 
<p>تسجيل الدخول</p>
<p>تسجيل الخروج</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># users_accounts/views.py</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>views <span class="token keyword">import</span> TokenObtainPairView<span class="token punctuation">,</span> TokenRefreshView</span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>tokens <span class="token keyword">import</span> RefreshToken</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib<span class="token punctuation">.</span>auth <span class="token keyword">import</span> get_user_model</span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> status</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>permissions <span class="token keyword">import</span> AllowAny</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>permissions <span class="token keyword">import</span> IsAuthenticated</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> render</span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>views <span class="token keyword">import</span> TokenObtainPairView</span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>serializers <span class="token keyword">import</span> TokenObtainPairSerializer</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>shortcuts <span class="token keyword">import</span> get_object_or_404</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">MyTokenObtainPairSerializer</span><span class="token punctuation">(</span>TokenObtainPairSerializer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">validate</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> attrs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        data <span class="token operator">=</span> <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>validate<span class="token punctuation">(</span>attrs<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># تحديث is_online عند تسجيل الدخول</span></span>
<span class="line">        user <span class="token operator">=</span> self<span class="token punctuation">.</span>user</span>
<span class="line">        user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">        user<span class="token punctuation">.</span>save<span class="token punctuation">(</span>update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'is_online'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> data</span>
<span class="line"></span>
<span class="line"><span class="token comment"># ✅ تسجيل الدخول</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">MyTokenObtainPairView</span><span class="token punctuation">(</span>TokenObtainPairView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> MyTokenObtainPairSerializer</span>
<span class="line"></span>
<span class="line"><span class="token comment"># ✅ تسجيل الخروج</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">LogoutAPIView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    permission_classes <span class="token operator">=</span> <span class="token punctuation">[</span>IsAuthenticated<span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">post</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        refresh_token <span class="token operator">=</span> request<span class="token punctuation">.</span>data<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">"refresh"</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">if</span> <span class="token keyword">not</span> refresh_token<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">"error"</span><span class="token punctuation">:</span> <span class="token string">"Refresh token is required."</span><span class="token punctuation">}</span><span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">try</span><span class="token punctuation">:</span></span>
<span class="line">            <span class="token comment"># Blacklist refresh token</span></span>
<span class="line">            token <span class="token operator">=</span> RefreshToken<span class="token punctuation">(</span>refresh_token<span class="token punctuation">)</span></span>
<span class="line">            token<span class="token punctuation">.</span>blacklist<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token comment"># تحديث حالة المستخدم</span></span>
<span class="line">            user <span class="token operator">=</span> request<span class="token punctuation">.</span>user</span>
<span class="line">            <span class="token keyword">if</span> user <span class="token keyword">and</span> user<span class="token punctuation">.</span>is_authenticated<span class="token punctuation">:</span></span>
<span class="line">                user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line">                user<span class="token punctuation">.</span>save<span class="token punctuation">(</span>update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">"is_online"</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"تم تسجيل الخروج بنجاح"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_200_OK<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token string">"error"</span><span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 📄 [ backend_django/urls.py ] ملف</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path<span class="token punctuation">,</span> include</span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>views <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    TokenObtainPairView<span class="token punctuation">,</span></span>
<span class="line">    TokenRefreshView<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>conf <span class="token keyword">import</span> settings</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>conf<span class="token punctuation">.</span>urls<span class="token punctuation">.</span>static <span class="token keyword">import</span> static</span>
<span class="line"><span class="token keyword">from</span> users_accounts<span class="token punctuation">.</span>views <span class="token keyword">import</span> MyTokenObtainPairView<span class="token punctuation">,</span>  LogoutAPIView</span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># simplejwt</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"api/login/"</span><span class="token punctuation">,</span> MyTokenObtainPairView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">"token_obtain"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"api/refresh/"</span><span class="token punctuation">,</span> TokenRefreshView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">"token_refresh"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"api/logout/"</span><span class="token punctuation">,</span> LogoutAPIView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">"logout"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token comment"># Admin</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">'admin/'</span><span class="token punctuation">,</span> admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>urls<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span> <span class="token operator">+</span> static<span class="token punctuation">(</span>settings<span class="token punctuation">.</span>MEDIA_URL<span class="token punctuation">,</span> document_root<span class="token operator">=</span>settings<span class="token punctuation">.</span>MEDIA_ROOT<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"><span class="token comment"># 📝 [users_accounts/signals.py] صفحة</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib<span class="token punctuation">.</span>auth<span class="token punctuation">.</span>signals <span class="token keyword">import</span> user_logged_in<span class="token punctuation">,</span> user_logged_out</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>dispatch <span class="token keyword">import</span> receiver</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token decorator annotation punctuation">@receiver</span><span class="token punctuation">(</span>user_logged_in<span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">def</span> <span class="token function">set_user_online</span><span class="token punctuation">(</span>sender<span class="token punctuation">,</span> request<span class="token punctuation">,</span> user<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">    user<span class="token punctuation">.</span>save<span class="token punctuation">(</span>update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'is_online'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token decorator annotation punctuation">@receiver</span><span class="token punctuation">(</span>user_logged_out<span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">def</span> <span class="token function">set_user_offline</span><span class="token punctuation">(</span>sender<span class="token punctuation">,</span> request<span class="token punctuation">,</span> user<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line">    user<span class="token punctuation">.</span>save<span class="token punctuation">(</span>update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'is_online'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


