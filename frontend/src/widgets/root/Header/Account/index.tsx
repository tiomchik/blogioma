import React, { useContext } from "react";
import { Link } from "@tanstack/react-router";
import { AuthContext } from "@/app/contexts";
import Pfp from "./Pfp";
import "./index.scss";

const Account: React.FC = () => {
  const { user } = useContext(AuthContext);

  if (user?.username) {
    return (
      <div className="account">
        <Link to="/auth/logout">Log out </Link> ||{" "}
        <Link to="/profile/$username" params={{ username: user?.username }} className="account-link">
          {user?.username}
          <Pfp />
        </Link>
      </div>
    );
  }

  return (
    <p>
      <Link to="/auth/sign_up">Sign up</Link> ||{" "}
      <Link to="/auth/login">Log in</Link>
    </p>
  );
};

export default Account;
