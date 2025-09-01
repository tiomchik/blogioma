import { expect, test, vi } from "vitest";
import { createDummyFile } from "@/tests/utils";
import axios from "axios";
import { createUser } from "./";
import { REGISTER_URL } from "./constants";

vi.mock("axios", () => {
  return { default: { post: vi.fn(() => ({ data: userData })) } };
});

const mockAxiosPost = vi.mocked(axios.post);

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

  const newUser = await createUser(formData);

  expect(mockAxiosPost).toHaveBeenCalledWith(REGISTER_URL, formData);
  expect(newUser).toEqual(userData);
});
