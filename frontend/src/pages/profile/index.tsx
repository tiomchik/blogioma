import { useAuth } from "@/app/contexts";
import {
  ProfileArea,
  ProfileContent,
  ProfileNavigation,
  ProfilePageHeading,
} from "@/widgets/profile";
import { useParams } from "@tanstack/react-router";
import React from "react";

const ProfilePage: React.FC = () => {
  const { currentUser } = useAuth();
  const { username } = useParams({ from: "/profile/$username/" });

  const isCurrentUserProfile = () => {
    return currentUser?.username === username;
  }

  return (
    <main>
      <div className="container">
        <ProfilePageHeading />
        <ProfileArea>
          {isCurrentUserProfile() && <ProfileNavigation />}
          <ProfileContent />
        </ProfileArea>
      </div>
    </main>
  );
};

export default ProfilePage;
