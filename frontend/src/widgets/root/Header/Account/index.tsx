import React from "react";
import { Link } from "@tanstack/react-router";
import { useAuth } from "@/app/contexts";
import Pfp from "@/shared/components/Pfp";
import "./index.scss";

const Account: React.FC = () => {
  const { currentUser } = useAuth();

  if (currentUser) {
    return (
      <div className="account">
        <Link to="/auth/logout">Log out </Link> ||{" "}
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
    <p>
      <Link to="/auth/sign_up">Sign up</Link> ||{" "}
      <Link to="/auth/log_in">Log in</Link>
    </p>
  );
};

export default Account;
