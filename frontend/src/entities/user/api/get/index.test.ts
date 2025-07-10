import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import { getUserByToken, getUserFromCookies } from "./";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return { default: { get: vi.fn(() => ({ data: expectedUser })) } };
});

const expectedUser = { username: "username", pfp: "/pfp.png" };

const mockedAxiosGet = vi.mocked(axios.get);

describe("getUserFromCookies", () => {
  test("user data has been loaded", async () => {
    cookies.set("token", "token");
    const user = await getUserFromCookies();
    expect(user).toEqual(expectedUser);
  });

  test("user data has not been loaded without token", async () => {
    cookies.remove("token");
    const user = await getUserFromCookies();
    expect(user).toEqual(null);
  });
});

describe("getUserByToken", () => {
  test("user has been received", async () => {
    const token = "token";
    const user = await getUserByToken(token);
    expect(mockedAxiosGet).toBeCalledWith(
      `${import.meta.env.VITE_API_URL}/auth/me`,
      { headers: { Authorization: `Token ${token}` } }
    );
    expect(user).toEqual(expectedUser);
  });
});
