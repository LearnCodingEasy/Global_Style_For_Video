"""
pip install pyautogui
pip install pyperclip
pip install rich
pip install psutil

"""
# 1 📍 Step 1: Import Libraries
# 🖥️ لفتح التطبيقات أو تنفيذ أوامر النظام
import subprocess
# ⌨️ لمحاكاة الكتابة والنقر وإجراءات لوحة المفاتيح والفأرة
import pyautogui
# 📋 للتعامل مع النسخ واللصق النصوص
import pyperclip
# ⏳ لإضافة التأخيرات الزمنية أثناء تنفيذ الأوامر
import time
# 🎨 لتحسين عرض النصوص في واجهة الكونسول باستخدام التنسيقات
from rich.console import Console
# 📂 التعامل مع الملفات والمجلدات
import os
# ← علشان نتحقق إذا البرنامج شغال
import psutil
# ⏱️ لتسجيل التوقيتات
import json
import tkinter as tk
# 🖥️ لإنشاء واجهات المستخدم الرسومية Tkinter مكتبة
# 🎨📲 ttk و messagebox استيراد العناصر المتقدمة مثل الـ
# لتصميم عناصر واجهة المستخدم
from tkinter import ttk, messagebox

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________


# 2 📍 Step 2: Configuration
# 📄 اسم الملف الذي سيتم كتابة النصوص البرمجية بداخله
file_name = ""
project_name = ""
# 📊 قائمة لتخزين بيانات التوقيت الخاصة بكل خطوة في العملية
timing_data = []
# 🖥️ (Terminal) وحدة تحكم لإظهار رسائل ملونة في الطرفية
console = Console()
# ⚙️ التحكم في تفعيل أو تعطيل الكتابة التلقائية
enable_auto_write = True
# ⚡ سرعة التنقل بين الأسطر أو البحث داخل الصفحة (بالثواني)
speed_search_line = 0.1
# ⏳ وقت الانتظار قبل إظهار الكود بعد بدء العملية (بالثواني)
time_waiting_show_code = 2
# ⏱️ وقت انتظار قبل بدء العملية ككل (بالثواني)
time_waiting_to_start = 1
# ⌛ مدة قصيرة للانتظار أثناء تنفيذ الأوامر المختلفة (بالثواني)
time_waiting_v = 0.1
time_waiting_s = 0.1
time_waiting_enter = 0.1
# 🔍 مدة الانتظار قبل بدء البحث داخل الكود (بالثواني)
time_waiting_search_line = 0.1
# 🕐 تأخير إضافي بعد البحث عن السطر (بالثواني)
time_waiting_search_line_delay = 0.1
# ⌨️ وقت الانتظار أثناء كتابة السطر الذي تم العثور عليه (بالثواني)
time_waiting_search_line_typing = 0.1
# 📉 مدة الانتظار قبل تصغير أو إخفاء السطر الذي تم البحث عنه (بالثواني)
time_waiting_search_line_collapse = 0.1
# 🖥️ مدة الانتظار قبل إظهار أو إخفاء الطرفية (Terminal) (بالثواني)
time_waiting_toggle_terminal = 1
# ⏱️ يتم هنا تسجيل الوقت الحالي بدقة عالية لقياس مدة تشغيل الفيديو أو العملية لاحقًا
# يستخدم time.perf_counter() لأنه يعطي توقيت بدقة أجزاء من الثانية، وهو مناسب لحساب الزمن المستغرق
video_start_time = time.perf_counter()

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________


# 📍 Function


def write_like_typing_on_keypord(file_path, text, delay=0.0):
    """
    تكتب النص داخل الملف وتحاكي الكتابة الطبيعية على لوحة المفاتيح.
    :param file_path: اسم الملف الذي سيتم الكتابة فيه
    :param text: النص المراد كتابته
    :param delay: التأخير بين الحروف لمحاكاة الكتابة الطبيعية
    """
    if enable_auto_write:
        # فتح الملف في وضع الإضافة
        with open(file_path, "a") as file:
            for char in text:
                # ⌨️ محاكاة الكتابة الطبيعية
                pyautogui.typewrite(char)
                # 📝 كتابة النص داخل الملف
                file.write(char)
                # التأكد من حفظ النص مباشرة
                file.flush()
                # ⏳ التأخير بين الحروف
                time.sleep(delay)
            # 📝 الانتقال إلى سطر جديد بعد كتابة النص
            # pyautogui.write("\n")
        print(f"✅ Text written: {text}")
    else:
        print("❌ Auto write is disabled.")


def automate_action(action, *args, delay=1, typing_delay=0.01):
    """
    يقوم بتنفيذ الأوامر تلقائيًا مع إضافة تأخير اختياري.
    :param action: نوع الإجراء (hotkey, typewrite, press, print)
    :param args: المعاملات المطلوبة للإجراء
    :param delay: تأخير قبل التنفيذ (افتراضي 1 ثانية)
    :param typing_delay: تأخير بين الأحرف عند الكتابة لمحاكاة الكتابة الطبيعية (افتراضي 0.05 ثانية)
    """
    time.sleep(delay)
    if action == "hotkey":
        pyautogui.hotkey(*args)
    elif action == "typewrite":
        # كتابة كل حرف على حدة مع تأخير
        for char in args[0]:
            pyautogui.typewrite(char)
            time.sleep(typing_delay)
    elif action == "press":
        pyautogui.press(*args)
    elif action == "print":
        console.print(*args)


# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________

# 4 📍 Step 4: Open OBS
start_time = time.perf_counter() - video_start_time

# تشغيل OBS وبدء التسجيل
obs_exe = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
obs_dir = r"C:\Program Files\obs-studio\bin\64bit"
subprocess.Popen([obs_exe, "--startrecording"], cwd=obs_dir, shell=True)


def is_obs_running():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "obs64.exe" in process.info['name'].lower():
            return True
    return False


if not is_obs_running():
    subprocess.Popen([obs_exe, "--startrecording"], cwd=obs_dir, shell=True)
    print("✅ Launch OBS and start recording!")
else:
    print("✅ OBS actually works!")


def is_recording_started():
    obs_log_path = os.path.expanduser("~\\AppData\\Roaming\\obs-studio\\logs")
    if not os.path.exists(obs_log_path):
        return False

    latest_log = sorted(os.listdir(obs_log_path), reverse=True)[0]
    with open(os.path.join(obs_log_path, latest_log), "r", encoding="utf-8") as log_file:
        log_data = log_file.read()
        # تحقق من بداية التسجيل
        return "Recording START" in log_data


timeout = 15
elapsed_time = 0
while not is_recording_started() and elapsed_time < timeout:
    time.sleep(1)
    elapsed_time += 1

if is_recording_started():
    print("✅Registration has started successfully! The following commands can now be executed:.")
    # ✨ هنا يمكنك وضع الأوامر التالية بعد بدء التسجيل
else:
    print("⚠️ Registration did not start within the specified deadline!")

time.sleep(3)
print("✅ OBS is opened successfully!")
end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Run_Obs",
    "start_time": start_time,
    "end_time": end_time
})

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________


# 5 📍 Step 5: Open Vscode
start_time = time.perf_counter() - video_start_time
result = subprocess.run(["where", "code"], capture_output=True, text=True)
if result.returncode == 0:
    # عرض المسار إذا تم العثور على البرنامج
    print("✅ VS Code found:", result.stdout.strip())
else:
    # رسالة خطأ إذا لم يتم العثور على البرنامج
    print("❌ VS Code not found. Make sure it is installed.")

# learn
# AFAQE

subprocess.Popen(
    [
        "C:\\Users\\learn\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        "--new-window",
        ".",
    ]
)
end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Run_Vscode",
    "start_time": start_time,
    "end_time": end_time
})

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# 📍: Start Create Project

time.sleep(10)
start_time = time.perf_counter() - video_start_time
time.sleep(1)
# 💻 ShortCut: Open New Terminal [] افتح محطة اوامر جديدة
automate_action("hotkey", "ctrl", "shift", "`", delay=5)
time.sleep(1)
pyperclip.copy("""npm create vue@latest""")
time.sleep(1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(1)

print("Start Create Project!")

end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Run_Create_Project",
    "start_time": start_time,
    "end_time": end_time
})


# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# 📍: Start Create Project

time.sleep(3)
start_time = time.perf_counter() - video_start_time

time.sleep(1)
pyperclip.copy("""wavesurfer_vue""")
time.sleep(1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(0.1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(1)

print("Wite Project Name!")

end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Wite_Project_Name",
    "start_time": start_time,
    "end_time": end_time
})


# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# 📍: Start Choose Options Project
time.sleep(5)

start_time = time.perf_counter() - video_start_time

# Router
time.sleep(1)
automate_action("press", "down", delay=0.1)
automate_action("press", "down", delay=0.1)
time.sleep(0.1)
automate_action("press", "space", delay=0.1)

# Pinia
time.sleep(1)
automate_action("press", "down", delay=0.1)
time.sleep(0.1)
automate_action("press", "space", delay=0.1)

# ESLint
time.sleep(1)
automate_action("press", "down", delay=0.1)
automate_action("press", "down", delay=0.1)
automate_action("press", "down", delay=0.1)
time.sleep(0.1)
automate_action("press", "space", delay=0.1)


# Prettier
time.sleep(1)
automate_action("press", "down", delay=0.1)
time.sleep(0.1)
automate_action("press", "space", delay=0.1)


time.sleep(2)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(2)

print("Choose Options Project !")

end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Options_Project",
    "start_time": start_time,
    "end_time": end_time
})

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# 📍: Start Choose Options Project

time.sleep(3)
start_time = time.perf_counter() - video_start_time

# Oxlint
time.sleep(1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(1)


end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Options_Oxlint",
    "start_time": start_time,
    "end_time": end_time
})


# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# 📍: Start Install & Rn Project

time.sleep(3)
start_time = time.perf_counter() - video_start_time
time.sleep(1)
pyperclip.copy("""cd wavesurfer_vue""")
time.sleep(1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(0.1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(1)

pyperclip.copy("""npm install""")
time.sleep(1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(1)
# Enter الضغط على
automate_action("press", "enter", delay=1)
time.sleep(25)


pyperclip.copy("""npm run format""")
time.sleep(0.1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(0.1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(8)


pyperclip.copy("""npm run dev""")
time.sleep(0.1)
automate_action("hotkey", "ctrl", "v", delay=0.1)
time.sleep(0.1)
# Enter الضغط على
automate_action("press", "enter", delay=0.1)
time.sleep(5)


print("Install Project!")

end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Install_Project",
    "start_time": start_time,
    "end_time": end_time
})

# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________
# _______________________________________


# 📍: Stop OBS

# بعد ما تخلص تسجيل
# الوقت اللي عايز تنتظره قبل إيقاف التسجيل
start_time = time.perf_counter() - video_start_time
time.sleep(3)
# أو "obs.exe" حسب إصدار البرنامج
program_name = "obs64.exe"
# استخدام taskkill
os.system(f"taskkill /f /im {program_name}")
print("🛑 Recording stopped!")

end_time = time.perf_counter() - video_start_time
timing_data.append({
    "section": "Section_Close_Obs",
    "start_time": start_time,
    "end_time": end_time
})

# ________________________________________________________
# ________________________________________________________
# ________________________________________________________
# ________________________________________________________
# ________________________________________________________
# 11 📍 Step 11: Write Timings Json

# 🕓 MoviePy تحويل التوقيتات إلى تنسيق مفهوم لـ


def format_time(seconds):
    # تحويل الثواني إلى HH:MM:SS
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = round(seconds % 60, 2)
    return f"{hours:02}:{minutes:02}:{secs:05.2f}"


# 🗂️ تخزين التوقيتات بشكل MoviePy-friendly
moviepy_timings = []
for part in timing_data:
    start = part["start_time"] - \
        timing_data[0]["start_time"]  # تعويض الفرق من أول جزء
    end = part["end_time"] - timing_data[0]["start_time"]
    moviepy_timings.append({
        "section": part["section"],
        "start_time": format_time(start),
        "end_time": format_time(end)
    })

# 💾 حفظ التوقيتات في ملف JSON
with open("start_project_vue_Timings.json", "w") as f:
    json.dump(moviepy_timings, f, indent=4)

console.print("[bold green]🎬 MoviePy timings saved successfully![/bold green]")
for item in moviepy_timings:
    console.print(
        f"[cyan]{item['section']}[/cyan]: [green]{item['start_time']}[/green] --> [red]{item['end_time']}[/red]")
