import React from "react";
import SocialMediaLinks from "./SocialMediaLinks";
import UserPfpWithUsername from "./UserPfpWithUsername";
import { ProfileDataContext } from "./context";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "@tanstack/react-router";
import { getUserByName } from "@/entities/user/api";
import "./index.scss";

const ProfileInfo: React.FC = () => {
  const { username } = useParams({ from: "/profile/$username" });
  const {
    data: profileData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["profileInfo", username],
    queryFn: () => getUserByName(username),
  });

  if (isLoading) return <h1>Loading...</h1>;

  if (error) {
    if (error.message.includes("404")) return <NotFoundMessage />;
    return <h1>{error.message}</h1>;
  }

  return (
    <div className="profile-info">
      <ProfileDataContext value={profileData!}>
        <UserPfpWithUsername />
        <SocialMediaLinks />
      </ProfileDataContext>
    </div>
  );
};

const NotFoundMessage: React.FC = () => {
  return <h1 data-testid="not-found-msg">User not found</h1>;
};

export default ProfileInfo;
