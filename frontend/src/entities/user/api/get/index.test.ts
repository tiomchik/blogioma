import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import { getUserByName, getUserByToken, getUserFromCookies } from "./";
import { ME_URL, USERS_URL } from "./constants";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return { default: { get: vi.fn(() => ({ data: expectedUser })) } };
});

const expectedUser = { username: "username", pfp: "/pfp.png" };

const mockAxiosGet = vi.mocked(axios.get);

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
    expect(mockAxiosGet).toBeCalledWith(ME_URL, {
      headers: { Authorization: `Token ${token}` },
    });
    expect(user).toEqual(expectedUser);
  });
});

describe("getUserByName", () => {
  test("user has been received", async () => {
    const username = "test";
    const user = await getUserByName(username);
    expect(mockAxiosGet).toBeCalledWith(`${USERS_URL}/${username}/`);
    expect(user).toEqual(expectedUser);
  });
});
