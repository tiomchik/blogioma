import { expect, test, vi } from "vitest";
import { generateUserArticlesUrl } from "./urls";
import { getUserArticles } from "./";
import { getArticles } from "@/entities/article/api";

vi.mock("@/entities/article/api", async () => {
  const actual = await vi.importActual("@/entities/article/api");
  return { ...actual, getArticles: vi.fn(() => expectedData) };
});

const expectedData = "data";
const username = "username";

const mockGetArticles = vi.mocked(getArticles);

test("functions called properly", async () => {
  const data = await getUserArticles(username);
  expect(mockGetArticles).toBeCalledWith(
    generateUserArticlesUrl(username),
    undefined // options is undefined
  );
  expect(data).toBe(expectedData);
});

test("functions called properly with options", async () => {
  const options = { amount: 10, page: 2 };
  await getUserArticles(username, options);
  expect(mockGetArticles).toBeCalledWith(
    generateUserArticlesUrl(username),
    options
  );
});
