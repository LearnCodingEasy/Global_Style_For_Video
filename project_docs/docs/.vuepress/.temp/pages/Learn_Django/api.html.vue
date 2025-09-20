<template><div><h1 id="django-page-api" tabindex="-1"><a class="header-anchor" href="#django-page-api"><span>Django Page Api</span></a></h1>
<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  إنشاء العناصر المراية و طريقة العرض و الفلاتر
</div>
<h2 id="noremal" tabindex="-1"><a class="header-anchor" href="#noremal"><span>Noremal</span></a></h2>
<h3 id="all" tabindex="-1"><a class="header-anchor" href="#all"><span>All</span></a></h3>
<div style="font-size:1.2vw; padding: 2rem 0 0 0; font-weight: 900;">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># views.py</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>decorators <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    api_view<span class="token punctuation">,</span></span>
<span class="line">    authentication_classes<span class="token punctuation">,</span></span>
<span class="line">    permission_classes<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>http <span class="token keyword">import</span> JsonResponse</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Product</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> ProductSerializer</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🏷️ دالة لجلب جميع الفئات</span></span>
<span class="line"><span class="token comment"># 🛠️ فقط GET تعريف هذه الدالة كواجهة برمجية تدعم طلبات</span></span>
<span class="line"><span class="token decorator annotation punctuation">@api_view</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token string">"GET"</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment"># 🔓 عدم استخدام مصادقة</span></span>
<span class="line"><span class="token decorator annotation punctuation">@authentication_classes</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment"># 🔓 عدم استخدام تصاريح</span></span>
<span class="line"><span class="token decorator annotation punctuation">@permission_classes</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">def</span> <span class="token function">product_list</span><span class="token punctuation">(</span>request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># 📚 جلب كل الفئات</span></span>
<span class="line">    products <span class="token operator">=</span> Product<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token comment"># 🔄 serializer باستخدام  JSON تحويل البيانات إلى صيغة</span></span>
<span class="line">    serializer <span class="token operator">=</span> ProductSerializer<span class="token punctuation">(</span>products<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token comment"># 📤 JSON إعادة البيانات بصيغة</span></span>
<span class="line">    <span class="token comment"># return Response(serializer.data)</span></span>
<span class="line">    <span class="token keyword">return</span> JsonResponse<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">,</span> safe<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># views.py</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Product</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> ProductSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">product_list</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> Product<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>order_by<span class="token punctuation">(</span><span class="token string">'-created_at'</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> ProductSerializer</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="single" tabindex="-1"><a class="header-anchor" href="#single"><span>Single</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🧐 Django كائن يُستخدم لبناء استعلامات معقدة في</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>db<span class="token punctuation">.</span>models <span class="token keyword">import</span> Q</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 📚 دالة لجلب بيانات دورة معينة باستخدام المعرف (pk)</span></span>
<span class="line"><span class="token decorator annotation punctuation">@api_view</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token string">"GET"</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">def</span> <span class="token function">course_detail</span><span class="token punctuation">(</span>request<span class="token punctuation">,</span> pk<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    user_ids <span class="token operator">=</span> <span class="token punctuation">[</span>request<span class="token punctuation">.</span>user<span class="token punctuation">.</span><span class="token builtin">id</span><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">for</span> user <span class="token keyword">in</span> request<span class="token punctuation">.</span>user<span class="token punctuation">.</span>friends<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        user_ids<span class="token punctuation">.</span>append<span class="token punctuation">(</span>user<span class="token punctuation">.</span><span class="token builtin">id</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 📦 جلب الدورة إذا كان منشؤها موجودًا ضمن معرفات المستخدمين</span></span>
<span class="line">    <span class="token comment"># 🔍 البحث عن الدورة المحددة باستخدام شرط أن تكون منشأة بواسطة المستخدم أو أصدقائه.</span></span>
<span class="line">    course <span class="token operator">=</span> Course<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>Q<span class="token punctuation">(</span>created_by_id__in<span class="token operator">=</span><span class="token builtin">list</span><span class="token punctuation">(</span>user_ids<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>get<span class="token punctuation">(</span>pk<span class="token operator">=</span>pk<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 🎨 تحويل بيانات الدورة إلى JSON باستخدام الـ Serializer</span></span>
<span class="line">    course_serializer <span class="token operator">=</span> CourseDetailSerializer<span class="token punctuation">(</span>course<span class="token punctuation">)</span></span>
<span class="line">    course_data <span class="token operator">=</span> course_serializer<span class="token punctuation">.</span>data</span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 🔐 التحقق من إذا كان المستخدم مصرحًا له</span></span>
<span class="line">    <span class="token comment"># 🔐 التحقق من إذا كان المستخدم قد سجل الدخول</span></span>
<span class="line">    <span class="token keyword">if</span> request<span class="token punctuation">.</span>user<span class="token punctuation">.</span>is_authenticated<span class="token punctuation">:</span></span>
<span class="line">        <span class="token comment"># ✅ إذا كان مصرحًا له، يتم استخدام بيانات الدورة كما هي</span></span>
<span class="line">        course_data <span class="token operator">=</span> course_serializer<span class="token punctuation">.</span>data</span>
<span class="line">    <span class="token keyword">else</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token comment"># 🚫 إذا لم يكن مصرحًا له، تكون بيانات الدورة فارغة</span></span>
<span class="line">        course_data <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 📚 جلب جميع الدروس المرتبطة بالدورة</span></span>
<span class="line">    lesson <span class="token operator">=</span> course<span class="token punctuation">.</span>lessons<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token comment"># 🎨 تحويل بيانات الدروس إلى JSON باستخدام الـ Serializer</span></span>
<span class="line">    lesson_serializer <span class="token operator">=</span> LessonListSerializer<span class="token punctuation">(</span>lesson<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    lesson_data <span class="token operator">=</span> lesson_serializer<span class="token punctuation">.</span>data</span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 📝 إرجاع بيانات الدورة والدروس في صيغة JSON</span></span>
<span class="line">    <span class="token keyword">return</span> JsonResponse<span class="token punctuation">(</span></span>
<span class="line">        <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"course"</span><span class="token punctuation">:</span> course_data<span class="token punctuation">,</span>  <span class="token comment"># 📝 بيانات الدورة</span></span>
<span class="line">            <span class="token string">"lessons"</span><span class="token punctuation">:</span> lesson_data<span class="token punctuation">,</span>  <span class="token comment"># 📚 بيانات الدروس</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="viewsets" tabindex="-1"><a class="header-anchor" href="#viewsets"><span>viewsets</span></a></h2>
<h5 id="rest-framework-viewsets" tabindex="-1"><a class="header-anchor" href="#rest-framework-viewsets"><span>rest_framework viewsets</span></a></h5>
<h3 id="all-1" tabindex="-1"><a class="header-anchor" href="#all-1"><span>All</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Get All Data List By viewsets</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Vendor</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> VendorSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">vendorViews</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> Vendor<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> VendorSerializer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="single-1" tabindex="-1"><a class="header-anchor" href="#single-1"><span>Single</span></a></h3>
<h4 id="single-by-user-by-viewsets" tabindex="-1"><a class="header-anchor" href="#single-by-user-by-viewsets"><span>Single By User By viewsets</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Get All Data Created By User By viewsets</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Vendor</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> VendorSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">vendorViews</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> Vendor<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> VendorSerializer</span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get_queryset</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> self<span class="token punctuation">.</span>queryset<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>created_by<span class="token operator">=</span>self<span class="token punctuation">.</span>request<span class="token punctuation">.</span>user<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="create" tabindex="-1"><a class="header-anchor" href="#create"><span>Create</span></a></h3>
<h4 id="create-data-by-viewsets" tabindex="-1"><a class="header-anchor" href="#create-data-by-viewsets"><span>Create Data By viewsets</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Create Data By viewsets</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Vendor</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> VendorSerializer</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">vendorViews</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> Vendor<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> VendorSerializer</span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">perform_create</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> serializer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        serializer<span class="token punctuation">.</span>save<span class="token punctuation">(</span>created_by<span class="token operator">=</span>self<span class="token punctuation">.</span>request<span class="token punctuation">.</span>user<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


