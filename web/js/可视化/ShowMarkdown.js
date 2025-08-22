import { marked } from 'https://cdn.jsdelivr.net/npm/marked@12.0.0/+esm';

export default function(node) {
    // 设置节点大小
    node.size = [400, 350];

    // 创建DOM容器
    const domContainer = document.createElement("div");
    domContainer.className = "comfyui_for_academic-markdown-container";
    domContainer.style.border = "1px solid #222";
    domContainer.style.borderRadius = "4px";
    domContainer.style.padding = "10px";
    domContainer.style.overflow = "auto";
    domContainer.style.width = "100%";
    domContainer.style.boxSizing = "border-box";
    domContainer.style.backgroundColor = "#1a1a1a";
    domContainer.innerHTML = "<div></div>";
    
    // 添加Markdown样式
    const markdownStyle = document.createElement("style");
    markdownStyle.textContent = `
        .comfyui_for_academic-markdown-container h1 {
            color: #fff;
            font-size: 20px;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 2px solid #444;
        }
        .comfyui_for_academic-markdown-container h2 {
            color: #f0f0f0;
            font-size: 18px;
            font-weight: 600;
            margin-top: 14px;
            margin-bottom: 10px;
            padding-bottom: 4px;
            border-bottom: 1px solid #444;
        }
        .comfyui_for_academic-markdown-container h3 {
            color: #e0e0e0;
            font-size: 16px;
            font-weight: 600;
            margin-top: 12px;
            margin-bottom: 8px;
        }
        .comfyui_for_academic-markdown-container h4, .comfyui_for_academic-markdown-container h5, .comfyui_for_academic-markdown-container h6 {
            color: #d0d0d0;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 6px;
        }
        .comfyui_for_academic-markdown-container p {
            margin-bottom: 10px;
            line-height: 1.5;
            color: #e0e0e0;
            font-size: 13px;
        }
        .comfyui_for_academic-markdown-container strong {
            color: #fff;
            font-weight: 600;
        }
        .comfyui_for_academic-markdown-container em {
            color: #f0f0f0;
            font-style: italic;
        }
        .comfyui_for_academic-markdown-container code {
            background-color: #2d2d2d;
            color: #ff6b6b;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 11px;
            border: 1px solid #444;
        }
        .comfyui_for_academic-markdown-container pre {
            background-color: #2d2d2d;
            padding: 8px;
            border-radius: 4px;
            overflow-x: auto;
            border: 1px solid #444;
            margin: 8px 0;
        }
        .comfyui_for_academic-markdown-container pre code {
            background: none;
            border: none;
            padding: 0;
            color: #e0e0e0;
        }
        .comfyui_for_academic-markdown-container blockquote {
            border-left: 3px solid #4CAF50;
            padding-left: 12px;
            margin: 10px 0;
            color: #c0c0c0;
            background-color: rgba(76, 175, 80, 0.1);
            padding: 8px 12px;
            border-radius: 0 3px 3px 0;
            font-style: italic;
        }
        .comfyui_for_academic-markdown-container ul, .comfyui_for_academic-markdown-container ol {
            padding-left: 20px;
            margin: 8px 0;
        }
        .comfyui_for_academic-markdown-container li {
            margin-bottom: 4px;
            line-height: 1.4;
            color: #e0e0e0;
            font-size: 13px;
        }
        .comfyui_for_academic-markdown-container li::marker {
            color: #4CAF50;
        }
        .comfyui_for_academic-markdown-container a {
            color: #2196F3;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-bottom-color 0.2s;
        }
        .comfyui_for_academic-markdown-container a:hover {
            border-bottom-color: #2196F3;
        }
        .comfyui_for_academic-markdown-container table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
            border: 1px solid #444;
            font-size: 12px;
        }
        .comfyui_for_academic-markdown-container th, .comfyui_for_academic-markdown-container td {
            border: 1px solid #444;
            padding: 6px 8px;
            text-align: left;
        }
        .comfyui_for_academic-markdown-container th {
            background-color: #333;
            color: #fff;
            font-weight: 600;
        }
        .comfyui_for_academic-markdown-container td {
            background-color: #2a2a2a;
        }
        .comfyui_for_academic-markdown-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #444, transparent);
            margin: 16px 0;
        }
        .comfyui_for_academic-markdown-container img {
            max-width: 100%;
            height: auto;
            border-radius: 3px;
            margin: 6px 0;
        }
    `;
    document.head.appendChild(markdownStyle);
    
    // 添加DOM容器到节点
    node.addDOMWidget("markdown_widget", "Markdown Display", domContainer);
    
    // 节点执行完成后的回调
    node.onExecuted = function(message) {
        if (message?.data) {
            const htmlContent = marked.parse(message.data[0]);
            domContainer.innerHTML = htmlContent;
        }
    };
}