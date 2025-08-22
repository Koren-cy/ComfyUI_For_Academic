export class NodeRegistry {
    constructor(prefix) {
        this.prefix = prefix;
        this.nodes = new Map();
        this.loadNodes();
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

    async loadNodes() {
        await this.loadNodeFrom('可视化', 
            ['ShowDOM', 'ShowMarkdown', 'ShowWebpage', 'MarkdownEditor', 'ShowImage']);
        await this.loadNodeFrom('Matplotlib', 
            ['LinePlot', 'ScatterPlot', 'BarPlot', 'Histogram', 'PieChart',
            'Heatmap', 'ContourPlot', 'QuiverPlot', 'StreamPlot',
            'BoxPlot', 'ViolinPlot', 'DensityPlot', 'QQPlot',
            'PolarPlot', 'RadarChart', 'TernaryPlot', 'ParallelCoordinates', 'SankeyDiagram']);
        
    }

    async loadNodeFrom(path,nodeFiles){
        for (const nodeFile of nodeFiles) {
            const nodeClass = `${this.prefix}_${nodeFile}`;
            try {
                const module = await import(`./${path}/${nodeFile}.js`);
                if (module.default) {
                    this.register(nodeClass, module.default);
                }
            } catch (error) {
                console.warn(`Failed to load node: ${nodeClass}`, error);
            }
        }
    }
}