import { vi } from "vitest";

const mockRouterLib = {
  createRootRoute: vi.fn(),
  createRouter: vi.fn(),
  RouterProvider: vi.fn(),
  Link: vi.fn(({ children }) => children),
  useLocation: vi.fn(),
  useNavigate: vi.fn(),
};

const mockQueryLib = {
  useQuery: vi.fn(() => ({ data: { results: [] } })),
  useMutation: vi.fn(() => ({ mutate: vi.fn() })),
  QueryClient: vi.fn(),
  QueryClientProvider: vi.fn(({ children }) => children),
};

export { mockRouterLib, mockQueryLib };
