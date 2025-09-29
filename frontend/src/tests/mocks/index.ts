import { ServerArticleResponse } from "@/entities/article/types";
import { ServerUserResponse } from "@/entities/user/types";
import { vi } from "vitest";

const mockUser: ServerUserResponse = {
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
  Link: vi.fn(({ children }) => children),
  useLocation: vi.fn(),
  useNavigate: vi.fn(),
};

const mockArticle: ServerArticleResponse = {
  id: 1,
  heading: "article 1",
  full_text: "full text",
  pub_date: "2023-09-01T00:00:00.000Z",
  update: null,
  author: mockUser,
  viewings: 100000,
};

export { mockUser, mockRouterLib, mockArticle };
