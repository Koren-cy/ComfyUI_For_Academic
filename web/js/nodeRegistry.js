export class NodeRegistry {
    constructor(prefix) {
        this.nodes = new Map();
        this.loadNodes(prefix);
    }

    register(nodeClass, handler) {
        this.nodes.set(nodeClass, handler);
    }

    async handleNode(node) {
        const handler = this.nodes.get(node.comfyClass);
        if (handler) {
            await handler(node);
        }
    }

    async loadNodes(prefix) {
        const nodeFiles = ['ShowDOM', 'ShowMarkdown', 'ShowWebpage', 'MarkdownEditor', 'ShowImage'];
        
        for (const nodeFile of nodeFiles) {
            const nodeClass = `${prefix}_${nodeFile}`;
            try {
                const module = await import(`./nodes/${nodeFile}.js`);
                if (module.default) {
                    this.register(nodeClass, module.default);
                }
            } catch (error) {
                console.warn(`Failed to load node: ${nodeClass}`, error);
            }
        }
    }
}