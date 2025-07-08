import { describe, expect, test, vi } from "vitest";
import {
  createAndPopulateFormData,
  setErrorsFromResponse,
} from "./utils";
import { AxiosError } from "axios";

const data = {
  username: "username",
  password: "password",
  password1: "password",
};

describe("createAndPopulateFormData", () => {
  test("returns a FormData object with the correct data", () => {
    const formData = createAndPopulateFormData(data);
    expect(formData.get("username")).toBe(data.username);
    expect(formData.get("password")).toBe(data.password);
    expect(formData.get("password1")).toBe(data.password1);
    expect(formData.get("pfp")).toBeNull();
    expect(formData.get("email")).toBeNull();
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
