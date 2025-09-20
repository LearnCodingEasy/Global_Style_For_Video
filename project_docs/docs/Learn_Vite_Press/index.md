# Vite Press

## 0️⃣1️⃣ Create Vuepress

###### 🖥️ Create Vuepress

```cmd
npm init vuepress project_docs
```

###### 📁 Project Readmap

```
📁Project
┣ 📁 project_docs

┣ 📜 .gitignore
┣ 📜 LICENSE
┣ 📜 README.md
```

## 0️⃣2️⃣ Go To Vuepress

###### 🖥️ Command Path

```cmd
cd project_docs
```

## 0️⃣3️⃣ Install Sass

###### 🖥️ Install Sass

```cmd
npm install -D sass-embedded
```

## 0️⃣4️⃣ Create File

###### 📝 Create File [ index.md ] Inside Docs

```
index.md
```

```cmd
touch index.md
```

###### 📁 Project Readmap

```
📁Project
┣ 📁 project_docs
┃ ┣ 📂 .github
┃ ┣ 📂 Scripts
┃ ┃ ┣ 📂 docs
┃ ┃ ┃ ┣ 📂 .vuepress
┃ ┃ ┃ ┣ 📜 get-started.md
┃ ┃ ┃ ┣ 📜 index.md
┃ ┃ ┃ ┣ 📜 README.md
┃ ┣ 📂 node_modules
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 package.json
```

## 0️⃣5️⃣ Edit File

###### 📝 Edit File [ index.md ] Inside Docs > .vuepress > config.js

```js
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
```

###### 📁 Project Readmap

```
📁Project
┣ 📁 project_docs
┃ ┣ 📂 .github
┃ ┣ 📂 Scripts
┃ ┃ ┣ 📂 docs
┃ ┃ ┃ ┣ 📂 .vuepress
┃ ┃ ┃ ┃ ┣ 📂 .cache
┃ ┃ ┃ ┃ ┣ 📂 .temp
┃ ┃ ┃ ┃ ┣ 📜 config.js
┃ ┃ ┃ ┣ 📜 get-started.md
┃ ┃ ┃ ┣ 📜 index.md
┃ ┃ ┃ ┣ 📜 README.md
┃ ┣ 📂 node_modules
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 package.json
```

## 0️⃣6️⃣ Extra Style

###### 🖌️ Add Your Extra Style

- Create File In [.vuepress/styles/index.scss]

```text
styles/index.scss
```

```cmd
touch styles/index.scss
```

```scss
body {
  #app {
    .vp-theme-container {
      header {
        overflow: hidden;
        transition: all 0.5s linear;

        > span {
          display: inline-block;
          padding: 0.3rem 0.5rem;
          border-radius: 5px;
          margin-top: -0.2rem;
          transition: all 0.5s linear;
          box-shadow: 0px 0px 3px 1px #29976479;

          > .route-link {
            display: flex;
            align-items: center;
            .vp-site-logo {
              width: 50px;
              height: 35px;
              border-radius: 5px;
            }
            .vp-site-name {
              text-transform: capitalize;
            }
          }
        }
        > .vp-navbar-items-wrapper {
          nav {
            .vp-navbar-item {
              a {
                padding: 0.1rem 0.5rem;
                &.route-link-active {
                  border-bottom: 0.1rem solid #299764;
                  box-shadow: 0px 0px 3px 1px #2997649c;
                  border-radius: 5px;
                }
              }
            }
          }
          button {
            // border: 0.1rem solid #c0bfbf52;
            box-shadow: 0px 0px 3px 1px #299764a6;

            padding: 5px;
            border-radius: 5px;
          }
        }
      }
      aside {
        .vp-sidebar-items {
          > li {
            p {
              text-transform: capitalize;
            }
            > ul {
              > li {
                > a.active {
                  border-right: 0.4rem solid #299764;
                }
                > ul {
                  > li {
                    > a.active {
                      border-bottom: 0.4rem solid #299764;
                    }
                  }
                }
              }
            }
          }
        }
      }
      main.vp-page {
        > div {
          > div {
            h1 {
              text-align: center;
              font-size: 3vw;
              font-weight: bold;
              text-transform: capitalize;
            }
            h2 {
              font-size: 2vw;
              font-weight: bold;
              text-transform: capitalize;
            }
          }
        }
      }
    }
  }
}
```

###### 📁 Project Readmap

```
📁Project
┣ 📁 project_docs
┃ ┣ 📂 .github
┃ ┣ 📂 Scripts
┃ ┃ ┣ 📂 docs
┃ ┃ ┃ ┣ 📂 .vuepress
┃ ┃ ┃ ┃ ┣ 📂 .cache
┃ ┃ ┃ ┃ ┣ 📂 .temp
┃ ┃ ┃ ┃ ┣ 📂 styles
┃ ┃ ┃ ┃ ┃ ┣ 📜 index.scss
┃ ┃ ┃ ┃ ┣ 📜 config.js
┃ ┃ ┃ ┣ 📜 get-started.md
┃ ┃ ┃ ┣ 📜 index.md
┃ ┃ ┃ ┣ 📜 README.md
┃ ┣ 📂 node_modules
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 package.json
```

## 0️⃣7️⃣ Build Vue Press

###### 🖥️ Build Vue Press

```cmd
npm run docs:build
```

```
📁Project
┣ 📁 project_docs
┃ ┣ 📂 .github
┃ ┣ 📂 Scripts
┃ ┃ ┣ 📂 docs
┃ ┃ ┃ ┣ 📂 .vuepress
┃ ┃ ┃ ┃ ┣ 📂 .cache
┃ ┃ ┃ ┃ ┣ 📂 .temp
┃ ┃ ┃ ┃ ┣ 📂 dist
┃ ┃ ┃ ┃ ┣ 📂 styles
┃ ┃ ┃ ┃ ┃ ┣ 📜 index.scss
┃ ┃ ┃ ┃ ┣ 📜 config.js
┃ ┃ ┃ ┣ 📜 get-started.md
┃ ┃ ┃ ┣ 📜 index.md
┃ ┃ ┃ ┣ 📜 README.md
┃ ┣ 📂 node_modules
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 package.json
```

## 0️⃣ 8️⃣ Run Vue Press

###### 🖥️ Run Vue Press

```cmd
npm run docs:dev
```
