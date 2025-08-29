import { expect, test } from "vitest";
import {
  generateUserArticlesUrl,
  USERNAME_ERROR_TEXT,
  USERS_URL,
} from "./urls";

test("generate url successfully", () => {
  const username = "user";
  const url = generateUserArticlesUrl(username);
  expect(url).toBe(`${USERS_URL}/${username}/articles/`);
});

test("throws error if username is empty", () => {
  expect(() => generateUserArticlesUrl("")).toThrowError(USERNAME_ERROR_TEXT);
});

test("encodes username correctly", () => {
  const usernameWithSpaces = "username with spaces";
  const encodedUsernameWithSpaces = encodeURIComponent(usernameWithSpaces);
  const url = generateUserArticlesUrl(usernameWithSpaces);
  expect(url).toBe(`${USERS_URL}/${encodedUsernameWithSpaces}/articles/`);
});
