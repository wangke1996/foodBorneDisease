import React, { Component } from 'react';
import { Layout, Menu, Breadcrumb, Row, Col } from 'antd';
import './mainView.css';
import { BrowserRouter as Router, Route, Link, withRouter } from 'react-router-dom';
import { BugMenu } from "./bugDetail";
import { ChatRobot } from "./chatRobot";
const { Header, Content, Footer } = Layout;



const TopMenu = withRouter(({ history }) => {
    return (
        <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['/']}
            selectedKeys={[history.location.pathname]}
            style={{ lineHeight: '64px' }}
        >
                <Menu.Item key="/">
                    <Link to='/'></Link>
                    致病微生物
                </Menu.Item>
                <Menu.Item key="/QA">
                    <Link to="/QA"/>
                    智能问诊
                </Menu.Item>
        </Menu>

    );
})

export class MainView extends Component {

    render() {

        return (

            <Layout className="layout">
                <Header>
                    <div className="logo" />
                    <TopMenu />
                </Header>
                <Content style={{ padding: '0 50px' }}>
                    <div style={{ background: '#fff', padding: "24px 80px", minHeight: 600 }}>
                        <Route path='/' exact component={BugMenu}></Route>
                        <Route path='/QA' exact component={ChatRobot}></Route>
                    </div>
                    {/* <Breadcrumb style={{margin: '16px 0'}}>
                        <Breadcrumb.Item>Home</Breadcrumb.Item>
                        <Breadcrumb.Item>List</Breadcrumb.Item>
                        <Breadcrumb.Item>App</Breadcrumb.Item>
                    </Breadcrumb>
                    <div style={{background: '#fff', padding: "24px 80px" , minHeight: 500}}>
                        <Row type="flex" justify="start">
                            <Col span={8}><BugMenu/></Col>
                            <Col span={16}><ChatRobot/></Col>
                        </Row>
                    </div> */}
                </Content>
                <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
            </Layout>
        )

    }
}

export default withRouter(MainView)