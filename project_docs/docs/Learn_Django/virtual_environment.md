## Django

### 🖥️ Virtual Environment

<p dir='rtl' style='font-size:1.2rem; font-weight:600'>
  علشان أعزل المشروع بمكتباته وإصداراته،
  عن أي مشروع تاني على الجهاز.
</p>

#### Need Python

```cmd
python --version
```

```cmd
py --version
```

#### Pip Version

```
pip --version
```

#### 📦 Upgrade Pip ( If Necessary )

```
py -m pip install --upgrade pip
```

### 🖥️ Create

#### 📦 Install Virtualenv Globally [Old]

```
pip install virtualenv
```

#### 🖥️ Create Virtual Environment 🐍

- 📁 Create Virtualenv For Your Owner Project

```cmd
python -m venv venv
```

```
📁Project
┣ 📁 .git

┣ 📁 venv
┃ ┣ 📂 Include
┃ ┣ 📂 Lib
┃ ┣ 📂 Scripts
┃ ┃ ┣ 📜 activate
┃ ┃ ┣ 📜 ...
┃ ┣ 📜 .gitignore
┃ ┣ 📜 pyvenv.cfg

┣ 📜 .gitignore
┣ 📜 LICENSE
┣ 📜 README.md
```

### 🚀 Activate

#### 🚀 Activate Virtual Environment 🔋

```cmd
venv\Scripts\activate
```

### 📚 Show Libraries

##### 📚 Show Libraries List

```
pip list
```

```cmd
pip freeze
```

### ❌ Deactivate

##### Deactivate Virtual Environment

```
deactivate
```

### 🗑️ Remove

##### 🗑️ Remove Virtual Environment

```
rmdir /S /Q venv
```
