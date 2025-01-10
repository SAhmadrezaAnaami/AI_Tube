import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Input, Button, Table, notification, List, Typography, Spin, Modal, Badge } from 'antd';
import Cookies from 'js-cookie';

const { Sider, Content } = Layout;
const { Title } = Typography;
const { TextArea } = Input;

const SearchPage = () => {
    const [searchText, setSearchText] = useState('');
    const [videos, setVideos] = useState([]);
    const [searchHistory, setSearchHistory] = useState([]);
    const [points, setPoints] = useState(0);
    const [loading, setLoading] = useState(false);
    const [historyLoading, setHistoryLoading] = useState(true);
    const [selectedHistoryId, setSelectedHistoryId] = useState(null);
    const [showSearchInput, setShowSearchInput] = useState(true);
    const [downloadModalVisible, setDownloadModalVisible] = useState(false);
    const [downloadingVideoId, setDownloadingVideoId] = useState(null);
    const [videoBlobUrl, setVideoBlobUrl] = useState(null);

    // Configure Axios with Authorization Header
    const axiosInstance = axios.create({
        headers: {
            access_token: Cookies.get('token'),
        },
    });

    useEffect(() => {
        fetchSearchHistory();
    }, []);

    const fetchSearchHistory = async () => {
        try {
            const response = await axiosInstance.get('http://127.0.0.1:8000/status');
            if (response.data.status === 'success') {
                setSearchHistory(response.data.meta?.Search_record || []);
                setPoints(response.data.meta?.point_record || 0);
            }
        } catch (error) {
            notification.error({ message: 'Failed to fetch search history' });
        } finally {
            setHistoryLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/logout');
            if (response.status === 200) {
                Cookies.remove('token');
                notification.success({ message: 'Logged out successfully' });
                window.location.reload(); // Refresh the page to clear state
            }
        } catch (error) {
            notification.error({ message: 'Failed to log out. Please try again.' });
        }
    };

    const handleSearch = async () => {
        if (!searchText.trim()) {
            notification.warning({ message: 'Search text cannot be empty!' });
            return;
        }

        setLoading(true);
        try {
            const response = await axiosInstance.post('http://127.0.0.1:8000/search', { searchText });
            if (response.status === 200) {
                setVideos(response.data.data || []);
                notification.success({ message: 'Search completed successfully' });
                fetchSearchHistory(); // Update history after search
                setShowSearchInput(false); // Hide input after search
            }
        } catch (error) {
            notification.error({ message: 'Failed to search. Please try again.' });
        } finally {
            setLoading(false);
        }
    };

    const handleHistoryClick = async (id) => {
        setLoading(true);
        setSelectedHistoryId(id);
        setShowSearchInput(false);
        try {
            const response = await axiosInstance.get(`http://127.0.0.1:8000/search/${id}`);
            if (response.status === 200) {
                setVideos(response.data.data || []);
            }
        } catch (error) {
            notification.error({ message: 'Failed to fetch video data from history.' });
        } finally {
            setLoading(false);
        }
    };

    const handleBackToSearch = () => {
        setShowSearchInput(true);
        setVideos([]);
        setSelectedHistoryId(null);
    };

    const handleDownload = async (videoId) => {
        setDownloadingVideoId(videoId);
        try {
            const response = await axiosInstance.post('http://127.0.0.1:8000/video/download', { video_id: videoId }, { responseType: 'blob' });
            if (response.status === 200) {
                const blob = new Blob([response.data], { type: response.data.type });
                const blobUrl = URL.createObjectURL(blob);
                setVideoBlobUrl(blobUrl);
                setDownloadModalVisible(true);
            } else {
                notification.error({ message: 'Failed to download video. Please try again.' });
            }
        } catch (error) {
            notification.error({ message: 'Error downloading video.' });
        } finally {
            setDownloadingVideoId(null);
        }
    };

    const handleCancelModal = () => {
        setDownloadModalVisible(false);
        URL.revokeObjectURL(videoBlobUrl);
        setVideoBlobUrl(null);
    };

    const columns = [
        {
            title: 'Thumbnail',
            dataIndex: 'thumbnail',
            key: 'thumbnail',
            render: (thumbnail) => (
                <img
                    src={`data:image/jpeg;base64,${thumbnail}`}
                    alt="thumbnail"
                    style={{ width: '100px', height: '60px' }}
                />
            ),
        },
        { title: 'Title', dataIndex: 'title', key: 'title' },
        { title: 'Description', dataIndex: 'description', key: 'description' },
        { title: 'Duration', dataIndex: 'duration', key: 'duration' },
        { title: 'Creator', dataIndex: 'creator', key: 'creator' },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Button
                    type="primary"
                    onClick={() => handleDownload(record.id)}
                    loading={downloadingVideoId === record.id}
                >
                    Download
                </Button>
            ),
        },
    ];

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider width="25%" style={{ background: '#fff' }}>
                <div style={{ padding: '10px' }}>
                    <Title level={4}>Search History</Title>
                    {historyLoading ? (
                        <Spin size="large" />
                    ) : searchHistory.length === 0 ? (
                        <p>No searches yet.</p>
                    ) : (
                        <List
                            dataSource={searchHistory}
                            renderItem={(item) => (
                                <List.Item
                                    key={item.id}
                                    onClick={() => handleHistoryClick(item.id)}
                                    style={{
                                        cursor: 'pointer',
                                        backgroundColor: selectedHistoryId === item.id ? '#f0f0f0' : 'transparent',
                                    }}
                                >
                                    <List.Item.Meta
                                        title={<a>{item.search_text}</a>}
                                        description={`Searched on: ${new Date(item.created_at).toLocaleString()}`}
                                    />
                                </List.Item>
                            )}
                        />
                    )}
                </div>
            </Sider>
            <Layout>
                <Content style={{ padding: '24px', position: 'relative' }}>
                    {/* Points Display and Logout Button */}
                    <div style={{
                        position: 'absolute',
                        top: '20px',
                        right: '20px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        
                    }}>
                        <div style={{
                            backgroundColor: '#52c41a',
                            borderRadius : "10px",
                            padding: '8px',
                        }}>
                        <Badge style={{ color: 'white' }}>
                            🏆 Points {points.points}
                        </Badge>
                        </div>
                        <Button type="primary" danger onClick={handleLogout}>
                            Logout
                        </Button>
                    </div>

                    {showSearchInput ? (
                        <div style={{ marginBottom: '24px', marginTop: '50px' }}>
                            <TextArea
                                rows={4}
                                value={searchText}
                                onChange={(e) => setSearchText(e.target.value)}
                                placeholder="Enter your search text..."
                            />
                            <Button
                                type="primary"
                                style={{ marginTop: '10px' }}
                                onClick={handleSearch}
                                loading={loading}
                            >
                                Search
                            </Button>
                        </div>
                    ) : (
                        <Button type="default" onClick={handleBackToSearch} style={{ marginBottom: '24px' }}>
                            Back to Search
                        </Button>
                    )}
                    {videos.length > 0 ? (
                        <Table
                            columns={columns}
                            dataSource={videos}
                            rowKey="id"
                            loading={loading}
                            pagination={{ pageSize: 5 }}
                        />
                    ) : (
                        !loading && !showSearchInput && <p>No videos found. Try searching something!</p>
                    )}
                </Content>
            </Layout>
            <Modal
                title="Downloaded Video"
                visible={downloadModalVisible}
                onCancel={handleCancelModal}
                footer={null}
                width={800}
            >
                {videoBlobUrl && <video src={videoBlobUrl} controls width="100%" />}
                {!videoBlobUrl && loading && <Spin size="large" />}
            </Modal>
        </Layout>
    );
};

export default SearchPage;
