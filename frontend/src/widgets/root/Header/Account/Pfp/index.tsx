import { AuthContext } from "@/app/contexts";
import ProfileIcon from "./profile.svg?react";
import React, { useContext } from "react";
import "./index.scss";

const Pfp: React.FC = () => {
  const { user } = useContext(AuthContext);

  if (user?.pfp) {
    return (
      <div className="pfp-wrapper">
        <img
          src={user.pfp}
          className="pfp"
          alt="profile picture"
          title="profile picture"
          width="32"
          height="28"
        />
      </div>
    );
  }

  return (
    <div className="pfp-wrapper">
      <ProfileIcon title="profile icon" />
    </div>
  );
};

export default Pfp;
