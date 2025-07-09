import { ServerUserResponse } from "@/entities/user/types";
import axios from "axios";

const createUser = async (userData: FormData) => {
  const response = await axios.post<ServerUserResponse>(
    `${import.meta.env.VITE_API_URL}/auth/register/`,
    userData
  );
  return response;
};

export { createUser };
