import { User } from "@/app/types";
import { UseNavigateResult } from "@tanstack/react-router";
import axios from "axios";
import Cookies from "universal-cookie";

const cookies = new Cookies();

type ServerUserResponse = {
  id: number;
  username: string;
  last_login: string;
  is_staff: boolean;
  date_joined: string;
  email: string | null;
  pfp: string | null;
  youtube: string;
  tiktok: string;
  twitch: string;
  linkedin: string;
};

const createUser = async (userData: FormData) => {
  const response = await axios.post<ServerUserResponse>(
    `${import.meta.env.VITE_API_URL}/auth/register/`,
    userData
  );
  return response;
};

type UserData = {
  username: string;
  password: string;
  pfp?: FileList | null;
  email?: string | null;
};

const authenticateAndRedirectToHome = async (
  userData: UserData,
  setCurrentUser: CallableFunction,
  navigate: UseNavigateResult<string>
) => {
  const token = await obtainToken(userData.username, userData.password);
  setAuthToken(token);

  setCurrentUser({
    username: userData.username,
    pfp: userData.pfp?.item(0),
  });

  navigate({ to: "/" });
};

type ObtainTokenResponse = { token: string };

const obtainToken = async (username: string, password: string) => {
  const response = await axios.post<ObtainTokenResponse>(
    `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
    { username, password }
  );
  return response.data.token;
};

const setAuthToken = (token: string) => {
  cookies.set("token", token, { path: "/" });
  setAuthTokenInAxiosHeaders(token);
};

const setAuthTokenInAxiosHeaders = (token: string) => {
  axios.defaults.headers.common["Authorization"] = `Token ${token}`;
};

const getUserFromCookies = async (): Promise<User | null> => {
  const token: string | undefined = cookies.get("token");
  if (!token) return null;
  const { username, pfp } = await getUserByToken(token);
  return { username, pfp };
};

const getUserByToken = async (token: string) => {
  const response = await axios.get<ServerUserResponse>(
    `${import.meta.env.VITE_API_URL}/auth/me`,
    { headers: { Authorization: `Token ${token}` } }
  );
  return response.data;
};

export {
  createUser,
  obtainToken,
  setAuthToken,
  authenticateAndRedirectToHome,
  setAuthTokenInAxiosHeaders,
  getUserFromCookies,
};
