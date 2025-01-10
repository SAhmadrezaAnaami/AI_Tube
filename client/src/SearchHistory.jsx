import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { List, Typography, Spin } from 'antd';
import Cookies from "js-cookie";

const { Title } = Typography;

const SearchHistory = () => {
    const [searchHistory, setSearchHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // ارسال درخواست برای دریافت تاریخچه جستجوها
        const fetchSearchHistory = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/status',{
                    headers: {
                        access_token: Cookies.get("token")
                    }
                });
                if (response.data.status === 'success') {
                    setSearchHistory(response.data.meta?.Search_record || []);
                }
            } catch (error) {
                setError('Failed to fetch search history');
            } finally {
                setLoading(false);
            }
        };

        fetchSearchHistory();
    }, []);

    if (loading) {
        return <Spin size="large" />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div style={{ padding: '10px' }}>
            <Title level={4}>Search History</Title>
            {searchHistory.length === 0 ? (
                <p>No searches yet.</p>
            ) : (
                <List
                    dataSource={searchHistory}
                    renderItem={(item) => (
                        <List.Item key={item.id}>
                            <List.Item.Meta
                                title={<a href="#">{item.search_text}</a>}
                                description={`Searched on: ${new Date(item.created_at).toLocaleString()}`}
                            />
                        </List.Item>
                    )}
                />
            )}
        </div>
    );
};

export default SearchHistory;
