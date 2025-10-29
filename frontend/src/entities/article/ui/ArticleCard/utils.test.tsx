import { describe, expect, test } from "vitest";
import { formatDate, truncateWithEllipsis } from "./utils";

describe("truncateWithEllipsis", () => {
  test("truncates a string to the specified length", () => {
    const result = truncateWithEllipsis("This is a long string", 10);
    expect(result).toBe("This is a ...");
  });

  test("returns the original string if it's shorter than length", () => {
    const result = truncateWithEllipsis("short", 10);
    expect(result).toBe("short");
  });
});

describe("formatDate", () => {
  test("formats a date object to a string", () => {
    const date = new Date("2025-07-17T11:09:16.499078Z");
    const result = formatDate(date);
    expect(result).toBe("July 17, 2025, 14:9 a.m."); 
  });
})
