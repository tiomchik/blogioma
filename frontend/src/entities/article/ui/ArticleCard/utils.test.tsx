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
  test("returns formatted string without year if it's current year", () => {
    const date = new Date("2025-07-17T06:09:16.499078Z");
    const result = formatDate(date);
    expect(result).toBe("July 17, 09:09");
  });

  test("returns formatted string with year if it's not current year", () => {
    const date = new Date("2023-07-17T06:09:16.499078Z");
    const result = formatDate(date);
    expect(result).toBe("2023, July 17, 09:09");
  })
})
