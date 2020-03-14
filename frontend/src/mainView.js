import React, {Component} from 'react';
import {Layout, Menu, Breadcrumb, Row, Col} from 'antd';
import {Launcher} from 'react-chat-window'
import {getAnswer} from "./api";
import './mainView.css';
import {BugMenu} from "./bugDetail";

const {Header, Content, Footer} = Layout;

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
            getAnswer(this.state.messageList, (answer) => {
                console.log(answer);
                this._sendMessage(answer);
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

export class MainView extends Component {
    render() {
        return (
            <Layout className="layout">
                <Header>
                    <div className="logo"/>
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={['2']}
                        style={{lineHeight: '64px'}}
                    >
                        <Menu.Item key="1">致病微生物</Menu.Item>
                        <Menu.Item key="2">智能问诊</Menu.Item>
                    </Menu>
                </Header>
                <Content style={{padding: '0 50px'}}>
                    <Breadcrumb style={{margin: '16px 0'}}>
                        <Breadcrumb.Item>Home</Breadcrumb.Item>
                        <Breadcrumb.Item>List</Breadcrumb.Item>
                        <Breadcrumb.Item>App</Breadcrumb.Item>
                    </Breadcrumb>
                    <div style={{background: '#fff', padding: 24, minHeight: 500}}>
                        <Row type="flex" justify="start">
                            <Col span={16}><BugMenu/></Col>
                            <Col span={4}><ChatWindow/></Col>
                        </Row>

                    </div>
                </Content>
                <Footer style={{textAlign: 'center'}}>Ant Design ©2018 Created by Ant UED</Footer>
            </Layout>
        )
    }
}