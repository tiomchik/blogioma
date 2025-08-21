import { expect, test } from "vitest";
import { generateUserArticlesUrl, USERNAME_ERROR_TEXT } from "./urls";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

test("generate url successfully", () => {
  const username = "user";
  const url = generateUserArticlesUrl(username);
  expect(url).toBe(`${baseUrl}/${username}/articles/`);
});

test("throws error if username is empty", () => {
  expect(() => generateUserArticlesUrl("")).toThrowError(USERNAME_ERROR_TEXT);
});

test("encodes username correctly", () => {
  const usernameWithSpaces = "username with spaces";
  const url = generateUserArticlesUrl(usernameWithSpaces);
  expect(url).toBe(
    `${baseUrl}/${encodeURIComponent(usernameWithSpaces)}/articles/`
  );
});
