import { createRouterWithRootComponent } from "@/tests/utils";
import { QueryClient } from "@tanstack/react-query";
import { expect, test, vi } from "vitest";
import App from ".";
import { act, render, screen } from "@testing-library/react";
import {
  getUserFromCookies,
  setAuthTokenInAxiosHeaders,
} from "@/entities/user/api";

vi.mock("@/entities/user/api", async () => {
  return {
    obtainTokenFromCookies: vi.fn(() => expectedToken),
    getUserFromCookies: vi.fn(() => expectedUser),
    setAuthTokenInAxiosHeaders: vi.fn(),
  };
});

vi.mock("react", async () => {
  const actual = await vi.importActual("react");
  return {
    ...actual,
    useState: vi.fn(() => [null, mockedSetCurrentUser]),
  };
});

const expectedToken = "token";
const expectedUser = { username: "username", pfp: "pfp" };

const mockedGetUserFromCookies = vi.mocked(getUserFromCookies);
const mockedSetAuthTokenInAxiosHeaders = vi.mocked(setAuthTokenInAxiosHeaders);
const mockedSetCurrentUser = vi.fn();

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
  expect(mockedSetAuthTokenInAxiosHeaders).toBeCalledWith(expectedToken);
  expect(mockedSetCurrentUser).toBeCalledWith(expectedUser);
});

test("user wasn't loaded", async () => {
  mockedGetUserFromCookies.mockResolvedValueOnce(null);
  await renderApp();
  expect(mockedSetAuthTokenInAxiosHeaders).not.toBeCalled();
  expect(mockedSetCurrentUser).not.toBeCalled();
});
