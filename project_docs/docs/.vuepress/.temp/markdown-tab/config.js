import { CodeTabs } from "D:/Global_Style_For_Video/project_docs/node_modules/@vuepress/plugin-markdown-tab/lib/client/components/CodeTabs.js";
import { Tabs } from "D:/Global_Style_For_Video/project_docs/node_modules/@vuepress/plugin-markdown-tab/lib/client/components/Tabs.js";
import "D:/Global_Style_For_Video/project_docs/node_modules/@vuepress/plugin-markdown-tab/lib/client/styles/vars.css";

export default {
  enhance: ({ app }) => {
    app.component("CodeTabs", CodeTabs);
    app.component("Tabs", Tabs);
  },
};
