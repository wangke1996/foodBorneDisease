import React, {Component, useState, useEffect, useRef, useCallback} from 'react';
import {ForceGraph3D} from 'react-force-graph';
import SpriteText from 'three-spritetext';

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
                    sprite.color = node.color;
                    sprite.textHeight = 8;
                    return sprite;
                }}
                linkThreeObjectExtend={true}
                linkThreeObject={link => {
                    // extend link with text sprite
                    const sprite = new SpriteText(link.relation);
                    sprite.color = 'lightgrey';
                    sprite.textHeight = 5;
                    return sprite;
                }}
                linkPositionUpdate={(sprite, {start, end}) => {
                    const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
                        [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
                    })));

                    // Position sprite
                    Object.assign(sprite.position, middlePos);
                }}
                backgroundColor = {'rgba(0,0,0,0.1)'}
        // enableNodeDrag={false}
        // onNodeClick={this.handleClick}
        />
    )
    }
}