import { PageHeading } from "@/shared/components";
import { useParams } from "@tanstack/react-router";
import React from "react";

const ProfilePageHeading: React.FC = () => {
  const { username } = useParams({ from: "/profile/$username/" });
  return <PageHeading>{username}'s profile</PageHeading>;
};

export default ProfilePageHeading;
