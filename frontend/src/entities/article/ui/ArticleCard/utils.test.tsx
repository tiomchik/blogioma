import { describe, expect, test } from "vitest";
import { formatDate, isCurrentYear, truncateWithEllipsis } from "./utils";

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

const currentYear = new Date().getFullYear();

describe("formatDate", () => {
  test("returns formatted string without year if it's current year", () => {
    const date = new Date(`${currentYear}-07-17T06:09:16.499078Z`);
    const result = formatDate(date);
    expect(result).toBe("July 17, 09:09");
  });

  test("returns formatted string with year if it's not current year", () => {
    const date = new Date("2023-07-17T06:09:16.499078Z");
    const result = formatDate(date);
    expect(result).toBe("2023, July 17, 09:09");
  });
});

describe("isCurrentYear", () => {
  test("returns true if year is current year", () => {
    const result = isCurrentYear(currentYear);
    expect(result).toBe(true);
  });

  test("returns false if year is not current year", () => {
    const result = isCurrentYear(2023);
    expect(result).toBe(false);
  });
});
