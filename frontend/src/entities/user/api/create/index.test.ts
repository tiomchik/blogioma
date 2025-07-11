import { expect, test, vi } from "vitest";
import { createDummyFile } from "@/tests/utils";
import axios from "axios";
import { createUser } from "./";

vi.mock("axios", () => {
  return { default: { post: vi.fn(() => ({ data: userData })) } };
});

const mockedAxiosPost = vi.mocked(axios.post);

const userData = {
  username: "username",
  password: "12341234",
  email: "test@example.com",
  pfp: createDummyFile("pfp.png", "image/png"),
};

test("axios.post was called with the correct arguments", async () => {
  const formData = new FormData();
  formData.append("username", userData.username);
  formData.append("password", userData.password);
  formData.append("email", userData.email);
  formData.append("pfp", userData.pfp);

  const response = await createUser(formData);

  expect(mockedAxiosPost).toHaveBeenCalledWith(
    `${import.meta.env.VITE_API_URL}/auth/register/`,
    formData
  );
  expect(response.data).toEqual(userData);
});
