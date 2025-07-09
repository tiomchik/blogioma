export type ServerUserResponse = {
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

export type UserData = {
  username: string;
  password: string;
  pfp?: FileList | null;
  email?: string | null;
};

export type ObtainTokenResponse = { token: string };
