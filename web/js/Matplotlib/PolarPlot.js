export default function(node) {
    // 设置节点大小
    node.size = [400, 300];

    // 创建图片元素
    const img = document.createElement("img");
    img.style.objectFit = "contain";
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.border = "1px solid #333";
    img.style.borderRadius = "4px";
    img.style.backgroundColor = "#1a1a1a";
    
    // 添加图片容器到节点
    node.addDOMWidget("matplotlib_widget", "Polar Plot", img);
    
    // 节点执行完成后的回调
    node.onExecuted = function(message) {
        if (message?.data) {
            img.src = `data:image/png;base64,${message.data[0]}`;
        }
    };
}