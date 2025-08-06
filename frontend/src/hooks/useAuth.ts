// hooks/useAuth.ts
import { useState } from "react";

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    const token = sessionStorage.getItem("session_token");
    return !!token;
  });

  const login = (token: string) => {
    sessionStorage.setItem("session_token", token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    sessionStorage.removeItem("session_token");
    setIsAuthenticated(false);
  };

  const getToken = () => {
    return sessionStorage.getItem("session_token");
  };

  return { isAuthenticated, login, logout, getToken };
};
