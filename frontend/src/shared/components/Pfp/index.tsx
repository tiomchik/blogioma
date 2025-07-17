import React from "react";
import { ContextUser } from "@/app/contexts/auth";
import ProfileIcon from "./profile.svg?react";
import "./index.scss";

type Props = {
  pfp?: ContextUser["pfp"];
};

const Pfp: React.FC<Props> = ({ pfp }) => {
  if (pfp) {
    return (
      <div className="wrapper">
        <img
          src={pfp}
          className="pfp"
          alt="profile picture"
          title="profile picture"
        />
      </div>
    );
  }

  return (
    <div className="wrapper">
      <ProfileIcon title="profile icon" />
    </div>
  );
};

export default Pfp;
