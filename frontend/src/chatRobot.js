import React, {Component} from 'react';
import {Launcher} from 'react-chat-window';
import {ForceGraph} from "./forceGraph";
import {Row, Col} from 'antd';
import {getAnswerAndGraph} from "./api";

const robotAvatar = process.env.PUBLIC_URL + '/img/robot.svg';

class ChatWindow extends Component {
    constructor(props) {
        super(props);
        this.state = {
            messageList: [],
            isOpen: true
        };
    }

    _onMessageWasSent = (message) => {
        this.setState({
            messageList: [...this.state.messageList, message]
        }, () => {
            getAnswerAndGraph(this.state.messageList, (response) => {
                console.log(response);
                const {answer, graph, result} = response;
                this._sendMessage(answer);
                this.props.setGraphData(graph);
                if (result) {
                    console.log(result);
                }
            });
        });
    };
    _sendMessage = (text) => {
        if (text.length > 0) {
            this.setState({
                messageList: [...this.state.messageList, {
                    author: 'them',
                    type: 'text',
                    data: {text}
                }]
            })
        }
    };
    handleClick = () => {
        if (this.state.isOpen)
            this.setState({messageList: [], isOpen: false});
        else
            this.setState({isOpen: true})
    };

    render() {
        const {messageList, isOpen} = this.state;
        return (<div>
            <Launcher
                agentProfile={{
                    teamName: '智能问诊机器人',
                    imageUrl: robotAvatar
                }}
                onMessageWasSent={this._onMessageWasSent}
                messageList={messageList}
                isOpen={isOpen}
                handleClick={this.handleClick}
                showEmoji={false}
            />
        </div>)
    }
}

export class ChatRobot extends Component {
    state = {
        data: null
    };
    setGraphData = data => this.setState({data});

    render() {
        return (
            <Row type='flex' justify="start">
                <Col span={12}>
                    <ChatWindow setGraphData={this.setGraphData.bind(this)}/>
                </Col>
                <Col span={12}>
                    <ForceGraph data={this.state.data}/>
                </Col>
            </Row>
        )
    }
}