import { beforeEach, expect, test, vi } from "vitest";
import LogInForm from "./";
import {
  clickSubmitButton,
  createRouterWithRootComponent,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import {
  setAuthToken,
  authenticateAndRedirectToHome,
} from "@/entities/user/api";

vi.mock("@/entities/user/api", () => {
  return {
    setAuthToken: vi.fn(),
    authenticateAndRedirectToHome: vi.fn(),
    obtainToken: vi.fn(() => "token"),
  };
});

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return { ...actual, useNavigate: vi.fn(() => mockedNavigate) };
});

const mockedSetCurrentUser = vi.fn();
const mockedSetAuthToken = vi.mocked(setAuthToken);
const mockedAuthenticateAndRedirectToHome = vi.mocked(
  authenticateAndRedirectToHome
);
const mockedNavigate = vi.fn();

const router = createRouterWithRootComponent(<LogInForm />);

beforeEach(async () => {
  await renderWithRoutingAndAuth(router, {
    setCurrentUser: mockedSetCurrentUser,
  });
  pasteIntoFieldByLabelText("Username", userData.username);
  pasteIntoFieldByLabelText("Password", userData.password);
});

const userData = {
  username: "username",
  password: "password",
};

test("successful registration flow", async () => {
  await clickSubmitButton();
  expect(mockedAuthenticateAndRedirectToHome).toHaveBeenCalledWith(
    userData,
    mockedSetCurrentUser,
    mockedNavigate
  );
});

test("error from the server was displayed", async () => {
  mockedAuthenticateAndRedirectToHome.mockRejectedValueOnce({
    response: { data: { detail: "Invalid credentials" } },
  });
  await clickSubmitButton();
  expectErrorMessage(/Invalid credentials/);
  expect(mockedSetAuthToken).not.toHaveBeenCalled();
  expect(mockedSetCurrentUser).not.toHaveBeenCalled();
});
