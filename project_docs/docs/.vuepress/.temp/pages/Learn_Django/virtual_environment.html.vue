<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<h3 id="🖥️-virtual-environment" tabindex="-1"><a class="header-anchor" href="#🖥️-virtual-environment"><span>🖥️ Virtual Environment</span></a></h3>
<p dir='rtl' style='font-size:1.2rem; font-weight:600'>
  علشان أعزل المشروع بمكتباته وإصداراته،
  عن أي مشروع تاني على الجهاز.
</p>
<h4 id="need-python" tabindex="-1"><a class="header-anchor" href="#need-python"><span>Need Python</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">py --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="pip-version" tabindex="-1"><a class="header-anchor" href="#pip-version"><span>Pip Version</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📦-upgrade-pip-if-necessary" tabindex="-1"><a class="header-anchor" href="#📦-upgrade-pip-if-necessary"><span>📦 Upgrade Pip ( If Necessary )</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">py -m pip install --upgrade pip</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="🖥️-create" tabindex="-1"><a class="header-anchor" href="#🖥️-create"><span>🖥️ Create</span></a></h3>
<h4 id="📦-install-virtualenv-globally-old" tabindex="-1"><a class="header-anchor" href="#📦-install-virtualenv-globally-old"><span>📦 Install Virtualenv Globally [Old]</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip install virtualenv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="🖥️-create-virtual-environment-🐍" tabindex="-1"><a class="header-anchor" href="#🖥️-create-virtual-environment-🐍"><span>🖥️ Create Virtual Environment 🐍</span></a></h4>
<ul>
<li>📁 Create Virtualenv For Your Owner Project</li>
</ul>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m venv venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 .git</span>
<span class="line"></span>
<span class="line">┣ 📁 venv</span>
<span class="line">┃ ┣ 📂 Include</span>
<span class="line">┃ ┣ 📂 Lib</span>
<span class="line">┃ ┣ 📂 Scripts</span>
<span class="line">┃ ┃ ┣ 📜 activate</span>
<span class="line">┃ ┃ ┣ 📜 ...</span>
<span class="line">┃ ┣ 📜 .gitignore</span>
<span class="line">┃ ┣ 📜 pyvenv.cfg</span>
<span class="line"></span>
<span class="line">┣ 📜 .gitignore</span>
<span class="line">┣ 📜 LICENSE</span>
<span class="line">┣ 📜 README.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="🚀-activate" tabindex="-1"><a class="header-anchor" href="#🚀-activate"><span>🚀 Activate</span></a></h3>
<h4 id="🚀-activate-virtual-environment-🔋" tabindex="-1"><a class="header-anchor" href="#🚀-activate-virtual-environment-🔋"><span>🚀 Activate Virtual Environment 🔋</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="📚-show-libraries" tabindex="-1"><a class="header-anchor" href="#📚-show-libraries"><span>📚 Show Libraries</span></a></h3>
<h5 id="📚-show-libraries-list" tabindex="-1"><a class="header-anchor" href="#📚-show-libraries-list"><span>📚 Show Libraries List</span></a></h5>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip list</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="❌-deactivate" tabindex="-1"><a class="header-anchor" href="#❌-deactivate"><span>❌ Deactivate</span></a></h3>
<h5 id="deactivate-virtual-environment" tabindex="-1"><a class="header-anchor" href="#deactivate-virtual-environment"><span>Deactivate Virtual Environment</span></a></h5>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">deactivate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="🗑️-remove" tabindex="-1"><a class="header-anchor" href="#🗑️-remove"><span>🗑️ Remove</span></a></h3>
<h5 id="🗑️-remove-virtual-environment" tabindex="-1"><a class="header-anchor" href="#🗑️-remove-virtual-environment"><span>🗑️ Remove Virtual Environment</span></a></h5>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">rmdir /S /Q venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


