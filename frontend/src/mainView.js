import React, {Component} from 'react';
import {Layout, Menu, Breadcrumb, Row, Col} from 'antd';
import './mainView.css';
import {BugMenu} from "./bugDetail";
import {ChatRobot} from "./chatRobot";

const {Header, Content, Footer} = Layout;

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
                            <Col span={8}><BugMenu/></Col>
                            <Col span={16}><ChatRobot/></Col>
                        </Row>

                    </div>
                </Content>
                <Footer style={{textAlign: 'center'}}>Ant Design ©2018 Created by Ant UED</Footer>
            </Layout>
        )
    }
}