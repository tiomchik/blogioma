import React from "react";
import ProfileInfo from "./ProfileInfo";
import ProfileArticles from "../ProfileArticles";
import "./index.scss";

const ProfileContent: React.FC = () => {
  return (
    <div className="profile-content">
      <ProfileInfo />
      <ProfileArticles />
    </div>
  );
};

export default ProfileContent;
