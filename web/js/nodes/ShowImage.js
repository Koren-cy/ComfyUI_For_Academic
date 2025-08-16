export default function(node) {
    // 设置节点大小
    node.size = [300, 250];

    // 创建图片元素
    const img = document.createElement("img");
    img.style.objectFit = "contain";
    
    // 添加图片容器到节点
    node.addDOMWidget("image_widget", "Image Display", img);
    
    // 节点执行完成后的回调
    node.onExecuted = function(message) {
        if (message?.data) {
            img.src = `data:image/png;base64,${message.data[0]}`;
        }
    };
}