import json
import pyautogui
import time

# # حركة الماوس للركن العلوي الأيسر توقف السكربت
# pyautogui.FAILSAFE = True
# # وقفة نصف ثانية بعد كل أمر تلقائيًا
# pyautogui.PAUSE = 0.5

# # رجّع أبعاد الشاشة (width, height)
# print(pyautogui.size())
# # موقع الماوس الحالي
# print(pyautogui.position())
# time.sleep(1)

# __________________________________
# __________________________________
# __________________________________
# __________________________________
# __________________________________
# print("ضع الماوس على أي مكان في الشاشة…")
# time.sleep(2)

# try:
#     while True:
#         x, y = pyautogui.position()
#         # يحدث السطر فقط
#         print(f"X={x}, Y={y}", end="\r")
#         time.sleep(0.05)
# except KeyboardInterrupt:
#     print("\nتم الإيقاف")

# __________________________________
# __________________________________
# __________________________________
# __________________________________
# __________________________________


positions = {}

print("حط الماوس على المكان واضغط Enter علشان أسجّله.")
print("اكتب exit للخروج.")


while True:
    cmd = input("اسم الزر: ")

    if cmd == "exit":
        break

    x, y = pyautogui.position()
    positions[cmd] = [x, y]
    print(f"تم حفظ {cmd}: {x}, {y}")

with open("positions.json", "w") as f:
    json.dump(positions, f, indent=4)

print("تم الحفظ.")
