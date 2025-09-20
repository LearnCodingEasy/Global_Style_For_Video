// 📂 Project Name

// 🖌️ VuePress استيراد الثيم الافتراضي من
import { defaultTheme } from "@vuepress/theme-default";

// 🛠️ VuePress استيراد دالة تعريف إعدادات المستخدم في
import { defineUserConfig } from "vuepress";

// ⚡ VuePress لاستخدامه مع Vite استيراد
import { viteBundler } from "@vuepress/bundler-vite";

// 📄 تصدير إعدادات المستخدم الرئيسية
export default defineUserConfig({
  // 🌐 لغة الموقع
  lang: "en-US",

  // 📍 عنوان الموقع الرئيسي
  title: "Project Title",
  // 💬 وصف الموقع
  description: "Project Description",

  // 🛠️ إعدادات الثيم الافتراضي مع تخصيص بعض الخصائص

  theme: defaultTheme({
    // 📸 Project Logo
    // Default
    // logo: "https://vuejs.press/images/hero.png",
    logo: "../Images/Logo.png",

    // 🖱️ شريط التنقل في الموقع
    navbar: ["/", "/Learn_Django/index", "/Learn_Vue/index", "/get-started"],
  }),

  // ⚡ لبناء المشروع Vite استخدام الباني
  bundler: viteBundler(),
});
