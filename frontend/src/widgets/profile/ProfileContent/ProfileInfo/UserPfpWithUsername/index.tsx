import { Pfp } from "@/shared/components";
import { useProfileData } from "../../context";
import React from "react";
import "./index.scss";

const UserPfpWithUsername: React.FC = () => {
  const { pfp, username } = useProfileData();

  return (
    <div className="user-pfp-with-username">
      <Pfp pfp={pfp} />
      {username}
    </div>
  );
};

export default UserPfpWithUsername;
