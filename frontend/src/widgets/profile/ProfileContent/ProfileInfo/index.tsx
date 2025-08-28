import React from "react";
import SocialMediaLinks from "./SocialMediaLinks";
import UserPfpWithUsername from "./UserPfpWithUsername";
import { ProfileDataContext } from "./context";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "@tanstack/react-router";
import { getUserByName } from "@/entities/user/api";
import "./index.scss";

const ProfileInfo: React.FC = () => {
  const { username } = useParams({ from: "/profile/$username/" });
  const { data: profileData, isLoading } = useQuery({
    queryKey: ["profileInfo", username],
    queryFn: () => getUserByName(username),
  });

  if (isLoading) return "Loading...";

  return (
    <div className="profile-info">
      <ProfileDataContext value={profileData!}>
        <UserPfpWithUsername />
        <SocialMediaLinks />
      </ProfileDataContext>
    </div>
  );
};

export default ProfileInfo;
