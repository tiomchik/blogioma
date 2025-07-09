import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import {
  authenticateAndRedirectToHome,
  createUser,
  obtainToken,
  setAuthToken,
  setAuthTokenInAxiosHeaders,
} from "./";
import { createDummyFile } from "@/tests/utils";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return {
    default: {
      post: vi.fn(() => ({ data: { token: "token" } })),
      defaults: { headers: { common: {} } },
    },
  };
});

const expectedToken = "token";

const mockedAxiosPost = vi.mocked(axios.post);

describe("createUser", () => {
  test("axios.post was called with the correct arguments", async () => {
    const formData = new FormData();
    formData.append("username", "username");
    formData.append("password", "12341234");
    formData.append("email", "test@example.com");
    formData.append("pfp", createDummyFile("pfp.png", "image/png"));
    await createUser(formData);
    expect(mockedAxiosPost).toHaveBeenCalledWith(
      `${import.meta.env.VITE_API_URL}/auth/register/`,
      formData
    );
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

const checkAuthTokenInHeader = (token: string) => {
  expect(axios.defaults.headers.common["Authorization"]).toBe(`Token ${token}`);
};
