import React from "react";
import { Link, useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/app/contexts";
import Pfp from "@/shared/components/Pfp";
import { logOut } from "@/entities/user/api";
import "./index.scss";

const Account: React.FC = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  const onClick = () => {
    logOut();
    navigate({ reloadDocument: true });
  };

  if (currentUser) {
    return (
      <div className="account">
        <p className="clickable" onClick={onClick}>
          Log out
        </p>
        ||
        <Link
          to="/profile/$username"
          params={{ username: currentUser.username }}
          className="account-link"
        >
          {currentUser.username}
          <Pfp pfp={currentUser.pfp} />
        </Link>
      </div>
    );
  }

  return (
    <p className="account">
      <Link to="/auth/sign_up">Sign up</Link>
      ||
      <Link to="/auth/log_in">Log in</Link>
    </p>
  );
};

export default Account;
