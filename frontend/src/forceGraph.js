import React, {Component, useCallback} from 'react';
import {ForceGraph3D} from 'react-force-graph';
import SpriteText from 'three-spritetext';

function addOpacityToHexColor(color, opacity = 0.5, mode = '#rrggbbaa') {
    const opacityHex = Math.round(opacity * 255).toString(16);
    if (mode === "#rrggbbaa")
        return color + opacityHex;
    else
        return "#" + opacityHex + color.slice(1);
}

export class ForceGraph extends Component {
    // state = {data: {nodes: [{id: 0}], links: []}};
    // handleClick = node => {
    //     const {nodes, links} = this.state.data;
    //
    //     // Remove node on click
    //     const newLinks = links.filter(l => l.source !== node && l.target !== node); // Remove links attached to node
    //     const newNodes = nodes.slice();
    //     newNodes.splice(node.id, 1); // Remove node
    //     newNodes.forEach((n, idx) => {
    //         n.id = idx;
    //     }); // Reset node ids to array index
    //
    //     this.setState({data: {nodes: newNodes, links: newLinks}});
    // };
    //
    // componentDidMount() {
    //     setInterval(() => {
    //         // Add a new connected node every second
    //         const {nodes, links} = this.state.data;
    //         const id = nodes.length;
    //         const data = {
    //             nodes: [...nodes, {id}],
    //             links: [...links, {source: id, target: Math.round(Math.random() * (id - 1))}]
    //         };
    //         this.setState({data})
    //     }, 1000);
    //
    // }
    render() {
        const {data} = this.props;
        if (!data)
            return [];
        return (
            <ForceGraph3D
                graphData={data}
                width={window.innerWidth / 3}
                height={window.innerHeight}
                nodeAutoColorBy="group"
                nodeThreeObject={node => {
                    const sprite = new SpriteText(node.id);
                    sprite.color = node.new ? addOpacityToHexColor(node.color, 0.7) : node.color;
                    sprite.textHeight = node.new ? 5 : 7;
                    sprite.fontWeight = node.new ? 'normal' : 'bold';
                    return sprite;
                }}
                linkAutoColorBy='relation'
                linkThreeObjectExtend={true}
                linkThreeObject={link => {
                    // extend link with text sprite
                    const sprite = new SpriteText(link.relation);
                    sprite.color = link.new ? addOpacityToHexColor(link.color, 0.7) : link.color;
                    sprite.textHeight = link.new ? 3 : 5;
                    sprite.fontWeight = link.new ? 'normal' : 'bold';
                    return sprite;
                }}
                linkWidth={link => link.new ? 1 : 3}
                linkOpacity={0.3}
                linkPositionUpdate={(sprite, {start, end}) => {
                    const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
                        [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
                    })));

                    // Position sprite
                    Object.assign(sprite.position, middlePos);
                }}
                linkDirectionalParticles={link => link.new ? 0 : 3}
                linkDirectionalParticleWidth={2}
                linkDirectionalParticleSpeed={0.005}
                backgroundColor={'rgba(0,0,0,1)'}
                // enableNodeDrag={false}
                // onNodeClick={this.handleClick}
            />
        )
    }
}