import { UserData, ObtainTokenResponse } from "@/entities/user/types";
import { UseNavigateResult } from "@tanstack/react-router";
import Cookies from "universal-cookie";
import axios from "axios";

const cookies = new Cookies();

const AUTH_TOKEN_COOKIE_KEY = "token";

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

const obtainTokenFromCookies = () => cookies.get(AUTH_TOKEN_COOKIE_KEY);

const setAuthToken = (token: string) => {
  cookies.set(AUTH_TOKEN_COOKIE_KEY, token, { path: "/" });
  setAuthTokenInAxiosHeaders(token);
};

const setAuthTokenInAxiosHeaders = (token: string) => {
  axios.defaults.headers.common["Authorization"] = `Token ${token}`;
};

export {
  AUTH_TOKEN_COOKIE_KEY,
  authenticateAndRedirectToHome,
  obtainToken,
  obtainTokenFromCookies,
  setAuthToken,
  setAuthTokenInAxiosHeaders,
};
