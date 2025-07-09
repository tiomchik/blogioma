import { UserData, ObtainTokenResponse } from "@/entities/user/types";
import { UseNavigateResult } from "@tanstack/react-router";
import Cookies from "universal-cookie";
import axios from "axios";

const cookies = new Cookies();

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

const obtainToken = async (username: string, password: string) => {
  const response = await axios.post<ObtainTokenResponse>(
    `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
    { username, password }
  );
  return response.data.token;
};

const obtainTokenFromCookies = () => cookies.get("token");

const setAuthToken = (token: string) => {
  cookies.set("token", token, { path: "/" });
  setAuthTokenInAxiosHeaders(token);
};

const setAuthTokenInAxiosHeaders = (token: string) => {
  axios.defaults.headers.common["Authorization"] = `Token ${token}`;
};

export {
  authenticateAndRedirectToHome,
  obtainToken,
  obtainTokenFromCookies,
  setAuthToken,
  setAuthTokenInAxiosHeaders,
};
