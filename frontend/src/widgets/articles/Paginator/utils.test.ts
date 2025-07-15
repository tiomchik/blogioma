import { describe, expect, test } from "vitest";
import { hasManyPagesAfterCurrent, hasManyPagesBeforeCurrent } from "./utils";

describe("hasManyPagesBeforeCurrent", () => {
  test("should return true if there are many pages before current", () => {
    expect(hasManyPagesBeforeCurrent(5)).toBe(true);
  });

  test("should return false if there aren't many pages before current", () => {
    for (let i = 1; i <= 4; i++) {
      expect(hasManyPagesBeforeCurrent(i)).toBe(false);
    }
  });
});

describe("hasManyPagesAfterCurrent", () => {
  test("should return true if there are many pages after current", () => {
    expect(hasManyPagesAfterCurrent(1, 10)).toBe(true);
  });

  test("should return false if there aren't many pages after current", () => {
    for (let i = 7; i <= 10; i++) {
      expect(hasManyPagesAfterCurrent(i, 10)).toBe(false);
    }
  });
});
