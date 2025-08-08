import { ServerUserResponse } from "@/entities/user/types";
import { createContext, useContext } from "react";

const ProfileDataContext = createContext<ServerUserResponse | null>(null);

const useProfileData = () => {
  const context = useContext(ProfileDataContext);
  if (!context) {
    throw new Error("useProfileData must be used within a ProfileDataContext");
  }
  return context;
};

export { ProfileDataContext, useProfileData };
