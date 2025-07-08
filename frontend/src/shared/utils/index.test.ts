import { useLocation } from "@tanstack/react-router";
import { describe, expect, test, vi } from "vitest";
import { isOnPage } from "./";

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    useLocation: vi.fn(),
  };
});

vi.mocked(useLocation, { partial: true }).mockReturnValue({ pathname: "/" });

describe("isOnPage", () => {
  test("should return true if the current pathname matches the provided URL", () => {
    const result = isOnPage("/");
    expect(result).toBe(true);
  });

  test("should return false if the current pathname does not match the provided URL", () => {
    const result = isOnPage("/about");
    expect(result).toBe(false);
  });
});
