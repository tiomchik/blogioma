import { ServerUserResponse } from "@/entities/user/types";
import React from "react";
import ProfileInfo from "./ProfileInfo";
import { ProfileDataContext } from "./context";
import "./index.scss";

const ProfileContent: React.FC<ServerUserResponse> = (profileData) => {
  return (
    <div className="profile-content">
      <ProfileDataContext value={profileData}>
        <ProfileInfo />
      </ProfileDataContext>
    </div>
  );
};

export default ProfileContent;
