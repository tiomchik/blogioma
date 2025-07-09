import { expect, test, vi } from "vitest";
import { createDummyFile } from "@/tests/utils";
import axios from "axios";
import { createUser } from "./";

vi.mock("axios", () => {
  return { default: { post: vi.fn() } };
});

const mockedAxiosPost = vi.mocked(axios.post);

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
