import axios from "axios";
import { describe, expect, test, vi } from "vitest";
import { createUser, obtainToken } from "./";
import { createDummyFile } from "@/tests/utils";

vi.mock("axios", () => {
  return {
    default: {
      post: vi.fn(),
    },
  };
});

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
    mockedAxiosPost.mockResolvedValueOnce({ data: { token: "token" } });
    await obtainToken("username", "password");
    expect(mockedAxiosPost).toHaveBeenCalledWith(
      `${import.meta.env.VITE_API_URL}/auth/obtain-token/`,
      { username: "username", password: "password" }
    );
  });
});
