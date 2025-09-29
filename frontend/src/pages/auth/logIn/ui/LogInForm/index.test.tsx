import { beforeEach, expect, test, vi } from "vitest";
import LogInForm from "./";
import {
  clickSubmitButton,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithAuth,
} from "@/tests/utils";
import {
  setAuthToken,
  authenticateAndRedirectToHome,
} from "@/entities/user/api";
const { mockRouterLib } = await vi.hoisted(() => import("@/tests/mocks"));

vi.mock("@/entities/user/api", () => {
  return {
    setAuthToken: vi.fn(),
    authenticateAndRedirectToHome: vi.fn(),
    obtainToken: vi.fn(() => "token"),
  };
});

vi.mock("@tanstack/react-router", async () => {
  return { ...mockRouterLib, useNavigate: vi.fn(() => mockNavigate) };
});

const mockSetCurrentUser = vi.fn();
const mockSetAuthToken = vi.mocked(setAuthToken);
const mockAuthenticateAndRedirectToHome = vi.mocked(
  authenticateAndRedirectToHome
);
const mockNavigate = vi.fn();

const userData = {
  username: "username",
  password: "password",
};

beforeEach(async () => {
  await renderWithAuth(<LogInForm />, { setCurrentUser: mockSetCurrentUser });
  pasteIntoFieldByLabelText("Username", userData.username);
  pasteIntoFieldByLabelText("Password", userData.password);
});

test("successful registration flow", async () => {
  await clickSubmitButton();
  expect(mockAuthenticateAndRedirectToHome).toHaveBeenCalledWith(
    userData,
    mockSetCurrentUser,
    mockNavigate
  );
});

test("error from the server was displayed", async () => {
  mockAuthenticateAndRedirectToHome.mockRejectedValueOnce({
    response: { data: { detail: "Invalid credentials" } },
  });
  await clickSubmitButton();
  expectErrorMessage(/Invalid credentials/);
  expect(mockSetAuthToken).not.toHaveBeenCalled();
  expect(mockSetCurrentUser).not.toHaveBeenCalled();
});
