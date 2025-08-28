import { ServerUserResponse } from "@/entities/user/types";
import React from "react";
import ProfileInfo from "./ProfileInfo";
import { ProfileDataContext } from "./context";
import "./index.scss";
import ProfileArticles from "../ProfileArticles";

const ProfileContent: React.FC<ServerUserResponse> = (profileData) => {
  return (
    <div className="profile-content">
      <ProfileDataContext value={profileData}>
        <ProfileInfo />
        <ProfileArticles />
      </ProfileDataContext>
    </div>
  );
};

export default ProfileContent;
