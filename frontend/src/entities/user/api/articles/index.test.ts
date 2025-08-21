import { expect, test, vi } from "vitest";
import { generateUserArticlesUrl } from "./urls";
import { getUserArticles } from "./";
import axios from "axios";

vi.mock("axios", () => {
  return {
    default: { get: vi.fn(() => ({ data: expectedData })) },
  };
});

const expectedData = "data";
const username = "username";

const mockAxiosGet = vi.mocked(axios.get);

test("articles received successfully", async () => {
  const data = await getUserArticles(username);
  expect(mockAxiosGet).toBeCalledWith(generateUserArticlesUrl(username));
  expect(data).toBe(expectedData);
});
