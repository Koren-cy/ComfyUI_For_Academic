import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";
import { $el } from "/scripts/ui.js";
import { NodeRegistry } from "./nodeRegistry.js";

const nodeRegistry = new NodeRegistry('ComfyUI_For_Academic');

// 注册节点
app.registerExtension({
    name: "ComfyUI.academic",
    async nodeCreated(node) {
        await nodeRegistry.handleNode(node);
    },
});

// 注册编译按钮 // 这段代码来自https://github.com/pydn/ComfyUI-to-Python-Extension
app.registerExtension({
	name: "ComfyUI.academic.menu",
	commands: [
    	{ 
    	  	id: "academic.compile", 
    	  	label: "编译为python脚本", 
    	  	function: () => {
				var filename = prompt("脚本名: ");
				if(filename === undefined || filename === null || filename === "") {
					return
				}
					
				app.graphToPrompt().then(async (p) => {
					const json = JSON.stringify({name: filename + ".json", workflow: JSON.stringify(p.output, null, 2)}, null, 2); 
					var response = await api.fetchApi(`/comfyui_for_academic_compile`, { method: "POST", body: json });
					if(response.status == 200) {
						const blob = new Blob([await response.text()], {type: "text/python;charset=utf-8"});
						const url = URL.createObjectURL(blob);
						if(!filename.endsWith(".py")) {
							filename += ".py";
						}

						const a = $el("a", {
							href: url,
							download: filename,
							style: {display: "none"},
							parent: document.body,
						});
						a.click();
						setTimeout(function () {
							a.remove();
							window.URL.revokeObjectURL(url);
						}, 0);
					}
				});
			}
    	}
  	],
	init() {
		$el("style", {
			parent: document.head,
		});
	},
	menuCommands: [
    { 
      path: ["Academic"], 
      commands: ["academic.compile"] 
    }
  ]
});

// 添加全局自定义样式
const style = document.createElement("style");
style.textContent = `
    .comfyui-for-academic-dom-container {
        width: 100%;
    }
`;
document.head.appendChild(style);