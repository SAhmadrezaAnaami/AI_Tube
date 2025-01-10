import React, { useState } from "react";
import { Layout, Tabs, Form, Input, Button, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

const { Content } = Layout;

const AuthPage = () => {
    const [registerForm] = Form.useForm();
    const [loginForm] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState("login"); // تب فعال
    const navigate = useNavigate(); // برای هدایت به مسیر دیگر

    const handleRegister = async (values) => {
        setLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:8000/register", values);
            if (response.status === 200) {
                message.success("Registration successful! Please log in.");
                registerForm.resetFields();
                setActiveTab("login"); // تغییر تب به Login
            }
        } catch (error) {
            message.error("Registration failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = async (values) => {
        setLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:8000/login", values);
            if (response.status === 200 && response.data.meta?.jwt_token) {
                await Cookies.set("token", response.data.meta.jwt_token, { path: "/", secure: true });
                message.success("Login successful!");
                window.location.reload()
            } else {
                throw new Error("Token not received.");
            }
        } catch (error) {
            message.error("Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout style={{ height: "100vh", justifyContent: "center", alignItems: "center" }}>
            <Content style={{ width: "400px", padding: "20px", background: "#fff", borderRadius: "8px" }}>
                <Tabs activeKey={activeTab} onChange={setActiveTab} centered>
                    {/* تب ورود */}
                    <Tabs.TabPane tab="Login" key="login">
                        <Form
                            form={loginForm}
                            layout="vertical"
                            onFinish={handleLogin}
                            autoComplete="off"
                            style={{ marginTop: "20px" }}
                        >
                            <Form.Item
                                name="email"
                                label="Email"
                                rules={[
                                    { required: true, message: "Please enter your email!" },
                                    // { type: "email", message: "Please enter a valid email address!" },
                                ]}
                            >
                                <Input placeholder="Enter your email" />
                            </Form.Item>
                            <Form.Item
                                name="password"
                                label="Password"
                                rules={[{ required: true, message: "Please enter your password!" }]}
                            >
                                <Input.Password placeholder="Enter your password" />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit" block loading={loading}>
                                    Login
                                </Button>
                            </Form.Item>
                        </Form>
                    </Tabs.TabPane>

                    {/* تب ثبت‌نام */}
                    <Tabs.TabPane tab="Register" key="register">
                        <Form
                            form={registerForm}
                            layout="vertical"
                            onFinish={handleRegister}
                            autoComplete="off"
                            style={{ marginTop: "20px" }}
                        >
                            <Form.Item
                                name="username"
                                label="Username"
                                rules={[{ required: true, message: "Please enter your username!" }]}
                            >
                                <Input placeholder="Enter your username" />
                            </Form.Item>
                            <Form.Item
                                name="email"
                                label="Email"
                                rules={[
                                    { required: true, message: "Please enter your email!" },
                                    // { type: "email", message: "Please enter a valid email address!" },
                                ]}
                            >
                                <Input placeholder="Enter your email" />
                            </Form.Item>
                            <Form.Item
                                name="password"
                                label="Password"
                                rules={[{ required: true, message: "Please enter your password!" }]}
                            >
                                <Input.Password placeholder="Enter your password" />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit" block loading={loading}>
                                    Register
                                </Button>
                            </Form.Item>
                        </Form>
                    </Tabs.TabPane>
                </Tabs>
            </Content>
        </Layout>
    );
};

export default AuthPage;
