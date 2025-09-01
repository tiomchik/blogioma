import { createRouterWithRootComponent } from "@/tests/utils";
import { QueryClient } from "@tanstack/react-query";
import { expect, test, vi } from "vitest";
import App from ".";
import { act, render, screen } from "@testing-library/react";
import {
  obtainTokenFromCookies,
  setAuthTokenInAxiosHeaders,
} from "@/entities/user/api";

vi.mock("@/entities/user/api", async () => {
  return {
    obtainTokenFromCookies: vi.fn(() => expectedToken),
    getUserByToken: vi.fn(() => expectedUser),
    setAuthTokenInAxiosHeaders: vi.fn(),
  };
});

vi.mock("react", async () => {
  const actual = await vi.importActual("react");
  return {
    ...actual,
    useState: vi.fn(() => [null, mockSetCurrentUser]),
  };
});

const expectedToken = "token";
const expectedUser = { username: "username", pfp: "pfp" };

const mockObtainTokenFromCookies = vi.mocked(obtainTokenFromCookies);
const mockSetAuthTokenInAxiosHeaders = vi.mocked(setAuthTokenInAxiosHeaders);
const mockSetCurrentUser = vi.fn();

const queryClient = new QueryClient();
const router = createRouterWithRootComponent(<div>component</div>);

const renderApp = async () => {
  await act(async () => {
    render(<App queryClient={queryClient} router={router} />);
  });
};

test("app renders correctly", async () => {
  await renderApp();
  const renderedComponent = screen.getByText("component");
  expect(renderedComponent).toBeDefined();
});

test("user was loaded correctly", async () => {
  await renderApp();
  expect(mockSetAuthTokenInAxiosHeaders).toBeCalledWith(expectedToken);
  expect(mockSetCurrentUser).toBeCalledWith(expectedUser);
});

test("user wasn't loaded", async () => {
  mockObtainTokenFromCookies.mockReturnValueOnce(null);
  await renderApp();
  expect(mockSetAuthTokenInAxiosHeaders).not.toBeCalled();
  expect(mockSetCurrentUser).not.toBeCalled();
});
