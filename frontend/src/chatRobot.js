import React, { Component } from 'react';
import { Launcher } from 'react-chat-window';
import { ForceGraph } from "./forceGraph";
import { Row, Col, Modal, Typography, Spin, Icon} from 'antd';
import { getAnswerAndGraph, resetRobot } from "./api";
import { getBugDetail, } from "./api";
import {LoadingOutlined } from '@ant-design/icons'

const { Title, Paragraph, Text } = Typography;
const name = '名称', disease = '疾病';
const robotAvatar = process.env.PUBLIC_URL + '/img/robot.svg';





class ChildModal extends Component {
    state = { visible: false };
    showModal = () => {
        this.setState({
            visible: true,
        });
    };
    handleOk = e => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    handleCancel = e => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };
    render() {
        return (
            <Modal
                width={800}
                visible={this.state.visible}
                closable={true}
                destroyOnClose={true}
                footer={null}
                // onOk={this.handleOk} 
                onCancel={this.handleCancel}
            >
                {this.props.content}
            </Modal>
        )
    }
}


class ChatWindow extends Component {
    constructor(props) {
        super(props);
        this.state = {
            messageList: [],
            isOpen: true,
            loading: true,
            detail: {}
        };
        resetRobot(() => { this.setState({ loading: false }) });
    }


    _onMessageWasSent = (message) => {
        this.setState({
            messageList: [...this.state.messageList, message],
            loading:true
        }, () => {
            getAnswerAndGraph(this.state.messageList, (response) => {
                console.log(response);
                const { answer, graph, result } = response;
                this._sendMessage(answer);
                this.props.setGraphData(graph);
                this.setState({ loading: false })
                if (result) {
                    if (result.length > 0) {
                        // console.log(result)
                        getBugDetail(result[0], detail => {
                            console.log(detail);
                            
                            this.setState({ detail });
                            if(JSON.stringify(this.state.detail) != "{}"){
                                this.ChildModal.showModal()}
                        });
                       
                    }
                }
            });
        });
    };
    _sendMessage = (text) => {
        if (text) {
            if (text.length > 0) {
                this.setState({
                    messageList: [...this.state.messageList, {
                        author: 'them',
                        type: 'text',
                        data: { text }
                    }]
                })
            }
        }
    };
    handleClick = () => {
        if (this.state.isOpen)
            this.setState({ messageList: [], isOpen: false });
        else
            this.setState({ isOpen: true })
    };

    render() {
        const { messageList, isOpen, detail, loading } = this.state;
        const antIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;
        return (<div>
            <Spin spinning={this.state.loading} indicator={antIcon} size="large" delay={500}>
            <Launcher
                agentProfile={{
                    teamName: "智能问诊机器人",
                    imageUrl: robotAvatar
                }}
                onMessageWasSent={this._onMessageWasSent}
                messageList={messageList}
                isOpen={isOpen}
                handleClick={this.handleClick}
                showEmoji={false}
            />
            </Spin>
            <ChildModal
                ref={(ChildModal) => { this.ChildModal = ChildModal; }}
                content={<Typography>
                    <Title>{detail[name]}</Title>
                    {Object.entries(detail).map(([key, value]) => {
                        if (key === disease) {
                            return <Typography key={key}>
                                <Title level={3}>{key}</Title>
                                <ul>
                                    {value.map((d, i) => <li key={i}>
                                        <ul>{Object.entries(d).map(([k, v]) => <li key={k}>
                                            <Title level={4}>{k}</Title>
                                            <Paragraph>{v}</Paragraph>
                                        </li>)}</ul>
                                    </li>)}
                                </ul>
                            </Typography>;
                        } else {
                            if (value.trim() === '')
                                return {};
                            return <Typography key={key}>
                                <Title level={3}>{key}</Title>
                                <Paragraph ellipsis={{ rows: 3, expandable: true }}>{value}</Paragraph>
                            </Typography>;
                        }
                    })}
                </Typography>} />
        </div >)
    }
}

export class ChatRobot extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            node: null
        };
       
    }
    setGraphData = data => this.setState({ data });

    onNodeClick(node) {
        console.log(node)
        this.setState({ node })
        this.ChatWindow._onMessageWasSent({
            author: 'me',
            type: 'text',
            data: { 'text': node }
        })
    }

    render() {
        return (


            <Row type='flex' justify="start">

                <Col span={8}>
                        <ChatWindow
                            setGraphData={this.setGraphData.bind(this)}
                            switchNode={this.state.node}
                            ref={(ChatWindow) => { this.ChatWindow = ChatWindow; }} />

                </Col>
                <Col span={16}>
                    <ForceGraph data={this.state.data} getNodeName={(node) => {
                        this.onNodeClick(node)
                    }} />
                </Col>

            </Row>
        )
    }
}




