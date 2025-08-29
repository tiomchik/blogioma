import { Pfp } from "@/shared/components";
import { Link } from "@tanstack/react-router";
import SettingsIcon from "./settings.svg?react";
import React from "react";
import { useAuth } from "@/app/contexts";
import "./index.scss";

const ProfileNavigation: React.FC = () => {
  const { currentUser } = useAuth();

  return (
    <aside className="profile-nav">
      <ul>
        <li>
          <Link
            to="/profile/$username"
            search={{ page: 1 }}
            params={{ username: currentUser?.username as string }}
            data-testid="profile-link"
          >
            <Pfp pfp={currentUser?.pfp} />
            Profile
          </Link>
        </li>
        <li>
          <Link to="/profile/settings" data-testid="profile-settings-link">
            <div className="wrapper">
              <SettingsIcon />
            </div>
            Profile settings
          </Link>
        </li>
      </ul>
    </aside>
  );
};

export default ProfileNavigation;
