import axios from "axios";

type CreateUserResponse = {
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
  const response = await axios.post<CreateUserResponse>(
    `${import.meta.env.VITE_API_URL}/auth/register/`,
    userData
  );
  return response;
};

type ObtainTokenResponse = {
  token: string;
};

const obtainToken = async (username: string, password: string) => {
  const response = await axios.post<ObtainTokenResponse>(
    `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
    { username, password }
  );
  return response.data.token;
};

const setAuthToken = (token: string) => {
  localStorage.setItem("token", token);
  axios.defaults.headers.common["Authorization"] = `Token ${token}`;
};

export { createUser, obtainToken, setAuthToken };
