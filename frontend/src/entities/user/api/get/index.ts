import { ServerUserResponse } from "@/entities/user/types";
import { ContextUser } from "@/app/contexts/auth";
import { ME_URL } from "./constants";
import axios from "axios";
import Cookies from "universal-cookie";

const cookies = new Cookies();

const getUserFromCookies = async (): Promise<ContextUser | null> => {
  const token: string | undefined = cookies.get("token");
  if (!token) return null;
  const { username, pfp } = await getUserByToken(token);
  return { username, pfp };
};

const getUserByToken = async (token: string) => {
  const response = await axios.get<ServerUserResponse>(ME_URL, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export { getUserFromCookies, getUserByToken };
