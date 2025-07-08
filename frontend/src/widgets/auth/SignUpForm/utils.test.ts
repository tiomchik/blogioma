import { describe, expect, test } from "vitest";
import { createAndPopulateFormData } from "./utils";

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
