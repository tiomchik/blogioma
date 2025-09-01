import { vi } from "vitest";

const mockUser = {
  id: 1,
  username: "username",
  pfp: "path/to/pfp.jpg",
  email: null,
  last_login: "",
  is_staff: false,
  date_joined: "",
  youtube: "https://www.youtube.com/",
  tiktok: "https://tiktok.com/",
  twitch: "https://twitch.tv/",
  linkedin: "https://linkedin.com/",
};

const mockRouterLib = {
  createRootRoute: vi.fn(),
  createRouter: vi.fn(),
  RouterProvider: vi.fn(),
  Link: vi.fn(),
};

export { mockUser, mockRouterLib };
