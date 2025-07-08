import { useLocation } from "@tanstack/react-router";
import { describe, expect, test, vi } from "vitest";
import { isOnPage, setErrorsFromResponse } from "./";
import { AxiosError } from "axios";

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

describe("setErrorsFromResponse", () => {
  const mockedSetError = vi.fn();

  test("sets field errors correctly", () => {
    const error = {
      response: {
        data: {
          username: ["This field is required."],
          password: ["This field is required."],
        },
      },
    } as AxiosError;

    setErrorsFromResponse(error, mockedSetError);

    expect(mockedSetError).toHaveBeenCalledWith("username", {
      message: "This field is required.",
    });
    expect(mockedSetError).toHaveBeenCalledWith("password", {
      message: "This field is required.",
    });
  });

  test("sets server error correctly", () => {
    const error = {
      response: { data: { detail: "error from the server" } },
    } as AxiosError;
    setErrorsFromResponse(error, mockedSetError);
    expect(mockedSetError).toHaveBeenCalledWith("root", {
      message: "error from the server",
    });
  });

  test("sets array of server errors correctly", () => {
    const error = {
      response: { data: { detail: ["error1", "error2"] } },
    } as AxiosError;
    setErrorsFromResponse(error, mockedSetError);
    expect(mockedSetError).toHaveBeenCalledWith("root", { message: "error1" });
    expect(mockedSetError).toHaveBeenCalledWith("root", { message: "error2" });
  });
});
