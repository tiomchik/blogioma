import React, { PropsWithChildren } from "react";
import "./index.scss";

const ProfileArea: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <div className="profile-area" data-testid="profile-area">
      {children}
    </div>
  );
};

export default ProfileArea;
