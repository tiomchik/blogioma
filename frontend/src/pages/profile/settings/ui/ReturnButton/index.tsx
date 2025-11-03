import React from "react";
import LeftArrowIcon from "./left-arrow.svg?react";
import { Link } from "@tanstack/react-router";
import { useAuth } from "@/app/contexts";

const ReturnButton: React.FC = () => {
  const { currentUser } = useAuth();

  if (!currentUser) return;

  return (
    <Link
      to="/profile/$username"
      params={{ username: currentUser.username }}
      data-testid="return-button"
    >
      <div className="wrapper">
        <LeftArrowIcon data-testid="return-icon" />
      </div>
    </Link>
  );
};

export default ReturnButton;
