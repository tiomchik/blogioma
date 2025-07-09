import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import {
  authenticateAndRedirectToHome,
  obtainToken,
  setAuthToken,
  setAuthTokenInAxiosHeaders,
} from "./";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return {
    default: {
      post: vi.fn(() => ({ data: { token: expectedToken } })),
      defaults: { headers: { common: {} } },
    },
  };
});

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
    expect(mockedSetCurrentUser).toHaveBeenCalledWith({
      username: data.username,
      pfp: undefined,
    });
    expect(mockedNavigate).toHaveBeenCalledWith({ to: "/" });
  });
});

describe("obtainToken", () => {
  test("axios.post was called with the correct arguments", async () => {
    await obtainToken("username", "password");
    expect(mockedAxiosPost).toHaveBeenCalledWith(
      `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
      { username: "username", password: "password" }
    );
  });
});

describe("setAuthToken", () => {
  test("auth token has been set", () => {
    setAuthToken(expectedToken);
    expect(cookies.get("token")).toBe(expectedToken);
    checkAuthTokenInHeader(expectedToken);
  });
});

describe("setAuthTokenInAxiosHeaders", () => {
  test("auth token has been set", () => {
    setAuthTokenInAxiosHeaders(expectedToken);
    checkAuthTokenInHeader(expectedToken);
  });
});

const checkAuthTokenInHeader = (token: string) => {
  expect(axios.defaults.headers.common["Authorization"]).toBe(`Token ${token}`);
};
