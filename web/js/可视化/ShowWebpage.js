export default function(node) {
    // 设置节点大小
    node.size = [350, 300];

    // 创建iframe容器
    const webContainer = document.createElement("div");
    webContainer.className = "comfyui_for_academic-web-container";
    webContainer.style.border = "1px solid #222";
    webContainer.style.borderRadius = "4px";
    webContainer.style.padding = "5px";
    webContainer.style.overflow = "hidden";
    webContainer.style.width = "100%";
    webContainer.style.height = "100%";
    webContainer.style.boxSizing = "border-box";
    webContainer.style.backgroundColor = "#1a1a1a";
    
    // 创建iframe元素
    const iframe = document.createElement("iframe");
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";
    iframe.style.borderRadius = "2px";
    iframe.src = "about:blank";
    iframe.sandbox = "allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox";
    
    // 添加容器到节点
    node.addDOMWidget("web_widget", "Webpage Display", webContainer);
    
    // 节点执行完成后的回调
    node.onExecuted = function(message) {
        if (message?.data) {            
            // 清空容器并添加iframe
            webContainer.innerHTML = "";
            
            // 设置iframe尺寸
            iframe.style.width = "100%";
            iframe.style.height = "100%";
            
            // 设置iframe源地址
            const url = message.data[0];
            iframe.src = url;

            webContainer.appendChild(iframe);
        }
    };
}