import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import { getUserFromCookies } from "./";
import Cookies from "universal-cookie";

const cookies = new Cookies();

vi.mock("axios", () => {
  return { default: { get: vi.fn() } };
});

const mockedAxiosGet = vi.mocked(axios.get);

describe("getUserFromCookies", () => {
  const expectedUser = { username: "username", pfp: "/pfp.png" };

  test("user data has been loaded", async () => {
    mockedAxiosGet.mockResolvedValue({ data: expectedUser });
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
