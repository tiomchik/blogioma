import { beforeEach, expect, test, vi } from "vitest";
import SignUpForm, { createAndPopulateFormData } from "./";
import { authenticateAndRedirectToHome } from "@/entities/user/api";
import {
  clickSubmitButton,
  createRouterWithRootComponent,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import {
  PASSWORD_CONFIRMATION_FIELD_LABEL,
  PASSWORD_FIELD_LABEL,
  USERNAME_FIELD_LABEL,
} from "@/shared/components";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createUser } from "@/entities/user/api";

vi.mock("@/entities/user/api", () => {
  return {
    createUser: vi.fn(),
    authenticateAndRedirectToHome: vi.fn(),
  };
});

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return { ...actual, useNavigate: vi.fn(() => mockNavigate) };
});

const mockCreateUser = vi.mocked(createUser);
const mockAuthenticateAndRedirectToHome = vi.mocked(
  authenticateAndRedirectToHome
);
const mockNavigate = vi.fn();
const mockSetCurrentUser = vi.fn();

const userData = {
  username: "username",
  email: "",
  password: "password",
  password1: "password",
};

const router = createRouterWithRootComponent(
  <QueryClientProvider client={new QueryClient()}>
    <SignUpForm />
  </QueryClientProvider>
);

beforeEach(async () => {
  await renderWithRoutingAndAuth(router, {
    setCurrentUser: mockSetCurrentUser,
  });

  pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, userData.username);
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, userData.password);
  pasteIntoFieldByLabelText(
    PASSWORD_CONFIRMATION_FIELD_LABEL,
    userData.password1
  );
});

test("successful registration flow", async () => {
  await clickSubmitButton();
  const formData = createAndPopulateFormData(userData);
  expect(mockCreateUser).toHaveBeenCalledWith(formData);
  expect(mockAuthenticateAndRedirectToHome).toHaveBeenCalledWith(
    { ...userData, pfp: expect.any(FileList) },
    mockSetCurrentUser,
    mockNavigate
  );
});

test("error from the server was displayed", async () => {
  mockCreateUser.mockRejectedValueOnce({
    response: { data: { detail: "error from the server" } },
  });
  await clickSubmitButton();
  expectErrorMessage(/error from the server/);
  expect(mockSetCurrentUser).not.toHaveBeenCalled();
});
