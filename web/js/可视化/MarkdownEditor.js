import { marked } from 'https://cdn.jsdelivr.net/npm/marked@12.0.0/+esm';

export default function(node) {
    // 设置节点大小
    node.size = [400, 350];

    // 创建主容器
    const mainContainer = document.createElement("div");
    mainContainer.className = "comfyui_for_academic-markdown-editor";
    mainContainer.style.border = "1px solid #222";
    mainContainer.style.borderRadius = "4px";
    mainContainer.style.overflow = "hidden";
    mainContainer.style.width = "100%";
    mainContainer.style.height = "100%";
    mainContainer.style.boxSizing = "border-box";
    mainContainer.style.backgroundColor = "#1a1a1a";
    mainContainer.style.display = "flex";
    mainContainer.style.flexDirection = "column";

    // 创建工具栏
    const toolbar = document.createElement("div");
    toolbar.style.padding = "8px";
    toolbar.style.borderBottom = "1px solid #333";
    toolbar.style.backgroundColor = "#2a2a2a";
    toolbar.style.display = "flex";
    toolbar.style.alignItems = "center";
    toolbar.style.gap = "10px";
    toolbar.style.fontSize = "12px";
    toolbar.style.color = "#ccc";
    mainContainer.appendChild(toolbar);

    // 创建模式切换按钮
    const modeToggle = document.createElement("button");
    modeToggle.textContent = "预览模式";
    modeToggle.style.padding = "4px 8px";
    modeToggle.style.border = "1px solid #555";
    modeToggle.style.borderRadius = "3px";
    modeToggle.style.backgroundColor = "#333";
    modeToggle.style.color = "#ccc";
    modeToggle.style.cursor = "pointer";
    modeToggle.style.fontSize = "11px";
    toolbar.appendChild(modeToggle);

    // 创建内容区域
    const contentArea = document.createElement("div");
    contentArea.style.flex = "1";
    contentArea.style.display = "flex";
    contentArea.style.overflow = "hidden";
    mainContainer.appendChild(contentArea);

    // 创建编辑器
    const editor = document.createElement("textarea");
    editor.style.width = "100%";
    editor.style.height = "100%";
    editor.style.border = "none";
    editor.style.outline = "none";
    editor.style.resize = "none";
    editor.style.padding = "10px 20px";
    editor.style.backgroundColor = "#1a1a1a";
    editor.style.color = "#e0e0e0";
    editor.style.fontSize = "13px";
    editor.style.fontFamily = "'Consolas', 'Monaco', 'Courier New', monospace";
    editor.style.lineHeight = "1.5";
    editor.placeholder = "在这里输入Markdown内容...";
    contentArea.appendChild(editor);

    // 创建预览区域
    const preview = document.createElement("div");
    preview.style.width = "100%";
    preview.style.height = "100%";
    preview.style.padding = "10px 35px";
    preview.style.backgroundColor = "#1a1a1a";
    preview.style.color = "#e0e0e0";
    preview.style.fontSize = "13px";
    preview.style.lineHeight = "1.5";
    preview.style.overflow = "auto";
    preview.style.display = "none";
    preview.innerHTML = "<p style='color: #888;'>预览将在这里显示...</p>";
    contentArea.appendChild(preview);
        
    // 存储当前的markdown内容
    let currentMarkdown = "";

    // 添加预览样式
    const previewStyle = document.createElement("style");
    previewStyle.textContent = `
        .comfyui_for_academic-markdown-editor h1 {
            color: #fff;
            font-size: 24px;
            font-weight: 600;
            margin-top: 24px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #444;
        }
        .comfyui_for_academic-markdown-editor h2 {
            color: #f0f0f0;
            font-size: 20px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 1px solid #444;
        }
        .comfyui_for_academic-markdown-editor h3 {
            color: #e0e0e0;
            font-size: 16px;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 10px;
        }
        .comfyui_for_academic-markdown-editor h4, .comfyui_for_academic-markdown-editor h5, .comfyui_for_academic-markdown-editor h6 {
            color: #d0d0d0;
            font-weight: 600;
            margin-top: 14px;
            margin-bottom: 8px;
        }
        .comfyui_for_academic-markdown-editor p {
            margin-bottom: 12px;
            line-height: 1.6;
            color: #e0e0e0;
        }
        .comfyui_for_academic-markdown-editor strong {
            color: #fff;
            font-weight: 600;
        }
        .comfyui_for_academic-markdown-editor em {
            color: #f0f0f0;
            font-style: italic;
        }
        .comfyui_for_academic-markdown-editor code {
            background-color: #2d2d2d;
            color: #ff6b6b;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            border: 1px solid #444;
        }
        .comfyui_for_academic-markdown-editor pre {
            background-color: #2d2d2d;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #444;
            margin: 12px 0;
        }
        .comfyui_for_academic-markdown-editor pre code {
            background: none;
            border: none;
            padding: 0;
            color: #e0e0e0;
        }
        .comfyui_for_academic-markdown-editor blockquote {
            border-left: 4px solid #4CAF50;
            padding-left: 16px;
            margin: 16px 0;
            color: #c0c0c0;
            background-color: rgba(76, 175, 80, 0.1);
            padding: 12px 16px;
            border-radius: 0 4px 4px 0;
            font-style: italic;
        }
        .comfyui_for_academic-markdown-editor ul, .comfyui_for_academic-markdown-editor ol {
            padding-left: 24px;
            margin: 12px 0;
        }
        .comfyui_for_academic-markdown-editor li {
            margin-bottom: 6px;
            line-height: 1.5;
            color: #e0e0e0;
        }
        .comfyui_for_academic-markdown-editor li::marker {
            color: #4CAF50;
        }
        .comfyui_for_academic-markdown-editor a {
            color: #2196F3;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-bottom-color 0.2s;
        }
        .comfyui_for_academic-markdown-editor a:hover {
            border-bottom-color: #2196F3;
        }
        .comfyui_for_academic-markdown-editor table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
            border: 1px solid #444;
        }
        .comfyui_for_academic-markdown-editor th, .comfyui_for_academic-markdown-editor td {
            border: 1px solid #444;
            padding: 8px 12px;
            text-align: left;
        }
        .comfyui_for_academic-markdown-editor th {
            background-color: #333;
            color: #fff;
            font-weight: 600;
        }
        .comfyui_for_academic-markdown-editor td {
            background-color: #2a2a2a;
        }
        .comfyui_for_academic-markdown-editor hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, #444, transparent);
            margin: 24px 0;
        }
        .comfyui_for_academic-markdown-editor img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 8px 0;
        }
    `;
    document.head.appendChild(previewStyle);    

    // 模式切换逻辑
    let isPreviewMode = false;
    modeToggle.onclick = function() {
        isPreviewMode = !isPreviewMode;
        if (isPreviewMode) {
            editor.style.display = "none";
            preview.style.display = "block";
            modeToggle.textContent = "编辑模式";
            // 更新预览内容
            if (currentMarkdown) {
                try {
                    preview.innerHTML = marked.parse(currentMarkdown);
                } catch (error) {
                    preview.innerHTML = `<p style='color: #ff6b6b;'>预览错误: ${error.message}</p>`;
                }
            }
        } else {
            editor.style.display = "block";
            preview.style.display = "none";
            modeToggle.textContent = "预览模式";
        }
    };

    // 编辑器内容变化监听
    editor.oninput = function() {
        currentMarkdown = editor.value;
        node.widgets[0].value = editor.value;
    };

    // 添加DOM容器到节点
    node.addDOMWidget("markdown_widget", "Markdown Editor", mainContainer);

    // 节点执行完成后的回调
    node.onExecuted = function(message) {
        if (message?.data && message.data[0] !== undefined) {
            const Content = message.data[0];
            editor.value = Content;
            currentMarkdown = Content;
        }
    };
}