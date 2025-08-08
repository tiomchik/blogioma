import React from "react";
import SocialMediaLinks from "./SocialMediaLinks";
import UserPfpWithUsername from "./UserPfpWithUsername";
import "./index.scss";

const ProfileInfo: React.FC = () => {
  return (
    <div className="profile-info">
      <UserPfpWithUsername />
      <SocialMediaLinks />
    </div>
  );
};

export default ProfileInfo;
