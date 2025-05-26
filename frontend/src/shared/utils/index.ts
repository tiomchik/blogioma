import { useLocation } from "@tanstack/react-router";

export const isOnPage = (url: string): boolean => {
  const location = useLocation();
  return location.pathname === url;
};
