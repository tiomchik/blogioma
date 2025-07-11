import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import {
  AUTH_TOKEN_COOKIE_KEY,
  authenticateAndRedirectToHome,
  logOut,
  obtainToken,
  obtainTokenFromCookies,
  setAuthToken,
  setAuthTokenInAxiosHeaders,
} from "./";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return {
    default: {
      get: vi.fn(() => ({ data: expectedUser })),
      post: vi.fn(() => ({ data: { token: expectedToken } })),
      defaults: { headers: { common: {} } },
    },
  };
});

const expectedUser = { username: "username", pfp: "pfp" };

const expectedToken = "token";

const mockedAxiosPost = vi.mocked(axios.post);

describe("authenticateAndRedirectToHome", () => {
  const data = {
    username: "username",
    password: "password",
    password1: "password",
  };

  test("all functions were called correctly", async () => {
    const mockedSetCurrentUser = vi.fn();
    const mockedNavigate = vi.fn();

    await authenticateAndRedirectToHome(
      data,
      mockedSetCurrentUser,
      mockedNavigate
    );

    checkAuthTokenInHeader(expectedToken);
    expect(mockedSetCurrentUser).toHaveBeenCalledWith(expectedUser);
    expect(mockedNavigate).toHaveBeenCalledWith({ to: "/" });
  });
});

describe("obtainToken", () => {
  test("axios.post was called with the correct arguments", async () => {
    const token = await obtainToken("username", "password");
    expect(mockedAxiosPost).toHaveBeenCalledWith(
      `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
      { username: "username", password: "password" }
    );
    expect(token).toBe(expectedToken);
  });
});

describe("obtainTokenFromCookies", () => {
  test("auth token has been got from cookies", () => {
    cookies.set(AUTH_TOKEN_COOKIE_KEY, expectedToken);
    expect(obtainTokenFromCookies()).toBe(expectedToken);
  });
});

describe("setAuthToken", () => {
  test("auth token has been set", () => {
    setAuthToken(expectedToken);
    expect(cookies.get(AUTH_TOKEN_COOKIE_KEY)).toBe(expectedToken);
    checkAuthTokenInHeader(expectedToken);
  });
});

describe("setAuthTokenInAxiosHeaders", () => {
  test("auth token has been set", () => {
    setAuthTokenInAxiosHeaders(expectedToken);
    checkAuthTokenInHeader(expectedToken);
  });
});

describe("logOut", () => {
  test("auth token has been removed", () => {
    setAuthToken(expectedToken);
    logOut();
    expect(cookies.get(AUTH_TOKEN_COOKIE_KEY)).toBeUndefined();
    expect(axios.defaults.headers.common["Authorization"]).toBeUndefined();
  });
});

const checkAuthTokenInHeader = (token: string) => {
  expect(axios.defaults.headers.common["Authorization"]).toBe(`Token ${token}`);
};
