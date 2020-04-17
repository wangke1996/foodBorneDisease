import React, {Component, useCallback} from 'react';
import {ForceGraph3D} from 'react-force-graph';
import SpriteText from 'three-spritetext';
import {ChatRobot} from './chatRobot'
function addOpacityToHexColor(color, opacity = 0.5, mode = '#rrggbbaa') {
    const opacityHex = Math.round(opacity * 255).toString(16);
    if (mode === "#rrggbbaa")
        return color + opacityHex;
    else
        return "#" + opacityHex + color.slice(1);
}



var color_dict = {"food":'rgba(255,215,0,1)',"disease":'rgba(65,105,225,1)',"time":'rgba(255,0,0,1)',"symptom":'rgba(60,179,113,1)'}

export class ForceGraph extends Component {

    // state = {data: {nodes: [{id: 0}], links: []}};
    // handleClick = node => {
    //     const {nodes, links} = this.data;
    
    //     // Remove node on click
    //     const newLinks = links.filter(l => l.source !== node && l.target !== node); // Remove links attached to node
    //     const newNodes = nodes.slice();
    //     newNodes.splice(node.id, 1); // Remove node
    //     newNodes.forEach((n, idx) => {
    //         n.id = idx;
    //     }); // Reset node ids to array index
    
    //     this.setState({data: {nodes: newNodes, links: newLinks}});

    // };
    // //
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

        constructor(props) {
        super(props);
    }

    handleClick = (node) =>{
        this.props.getNodeName(node);
    }
   
    render() {
        const {data} = this.props;
        if (!data)
            return [];
        return (
            <ForceGraph3D
                graphData={data}
                width={window.innerWidth / 2}
                height={window.innerHeight}
                nodeAutoColorBy="group"
                //nodeColor = {color_dict["group"]}
                nodeThreeObject={node => {
                    const sprite = new SpriteText(node.id);
                    sprite.color = node.new ? addOpacityToHexColor(node.color, 0.5) : node.color;
                    sprite.textHeight = node.new ? 7 : 5;
                    sprite.fontWeight = node.new ? 'bold' : 'normal';
                    return sprite;
                }}
                linkAutoColorBy='relation'
                linkThreeObjectExtend={true}
                linkThreeObject={link => {
                    // extend link with text sprite
                    const sprite = new SpriteText(link.index?link.index:"1");
                    sprite.color = link.new ? addOpacityToHexColor(link.color, 0.7) : link.color;
                    sprite.textHeight = link.index ? 0 : 3;
                    sprite.fontWeight = link.new ? 'normal' : 'bold';
                    return sprite;
                }}
                linkWidth={link => link.new ? 2: 1}
                linkOpacity={0.3}
                linkPositionUpdate={(sprite, {start, end}) => {
                    const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
                        [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
                    })));

                    // Position sprite
                    Object.assign(sprite.position, middlePos);
                }}
                linkDirectionalParticles={link => link.new ? 1 : 0}
                linkDirectionalParticleWidth={2}
                linkDirectionalParticleSpeed={0.005}
    
                backgroundColor={'rgba(255,255,255,0)'}
                // enableNodeDrag={false}
                onNodeClick={(node) => {
                    this.handleClick(node.id)}}
            />

        )
    }
}