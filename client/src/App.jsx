import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "./AuthPage";
import SearchPage from "./SearchPage";
import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode";

const isAuthenticated = () => {
    const token = Cookies.get("token");
    if (!token) return false;

    try {
        jwtDecode(token);
        return true;
    } catch (error) {
        Cookies.remove("token"); // توکن نامعتبر است
        return false;
    }
};

const App = () => {
    return (
        <Router>
            <Routes>
                {/* روت اصلی */}
                <Route
                    path="/"
                    element={
                        isAuthenticated() ? <Navigate to="/search" replace /> : <Navigate to="/auth" replace />
                    }
                />

                {/* روت auth */}
                <Route
                    path="/auth"
                    element={
                        isAuthenticated() ? <Navigate to="/search" replace /> : <AuthPage />
                    }
                />

                {/* روت search */}
                <Route
                    path="/search"
                    element={
                        isAuthenticated() ? <SearchPage /> : <Navigate to="/auth" replace />
                    }
                />

                {/* روت‌های دیگر */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </Router>
    );
};

export default App;
