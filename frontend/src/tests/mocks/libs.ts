import { vi } from "vitest";

const mockRouterLib = {
  createRootRoute: vi.fn(),
  createRouter: vi.fn(),
  RouterProvider: vi.fn(),
  Link: vi.fn(({ children }) => children),
  useLocation: vi.fn(),
  useNavigate: vi.fn(),
};

export { mockRouterLib };
