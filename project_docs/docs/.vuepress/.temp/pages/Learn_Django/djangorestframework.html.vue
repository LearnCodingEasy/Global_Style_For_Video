<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<h3 id="_1️⃣-install" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install"><span>1️⃣ Install</span></a></h3>
<div dir="rtl" style="font-size:1.5vw">
<p>هو إطار العمل اللي بيوفر لك الـ API نفسها، لكن مش مسؤول عن التحكم في السماح أو المنع بناءً على الدومين.</p>
</div>
<h4 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h4>
<div dir="rtl" style="font-size:1.5vw">
  افتح الـ Terminal في مشروع Django واكتب:
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<div dir="rtl" style="font-size:1.5vw">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Libraries</span></span>
<span class="line">  <span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="_3️⃣-used" tabindex="-1"><a class="header-anchor" href="#_3️⃣-used"><span>3️⃣ used</span></a></h3>
<div dir="rtl" style="font-size:1.5vw">
  استخدام APIView (التحكم الكامل):
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> status</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Post</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> PostSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">PostListCreateView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"><span class="token keyword">def</span> <span class="token function">get</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">posts <span class="token operator">=</span> Post<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">serializer <span class="token operator">=</span> PostSerializer<span class="token punctuation">(</span>posts<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">post</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        serializer <span class="token operator">=</span> PostSerializer<span class="token punctuation">(</span>data<span class="token operator">=</span>request<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">if</span> serializer<span class="token punctuation">.</span>is_valid<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">            serializer<span class="token punctuation">.</span>save<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_201_CREATED<span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>errors<span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size:1.5vw">
  استخدام ViewSets (الأفضل في المشاريع الكبيرة):
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Post</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> PostSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">PostViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">queryset <span class="token operator">=</span> Post<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">serializer_class <span class="token operator">=</span> PostSerializer</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


