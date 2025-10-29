import { beforeEach, expect, test, vi } from "vitest";
import SignUpForm, { createAndPopulateFormData } from "./";
import { authenticateAndRedirectToHome } from "@/entities/user/api";
import {
  clickSubmitButton,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithQueryClient,
} from "@/tests/utils";
import {
  PASSWORD_CONFIRMATION_FIELD_LABEL,
  PASSWORD_FIELD_LABEL,
  USERNAME_FIELD_LABEL,
} from "@/shared/components";
import { createUser } from "@/entities/user/api";
import { AuthContext } from "@/app/contexts";
const { mockRouterLib } = await vi.hoisted(() => import("@/tests/mocks"));

vi.mock("@/entities/user/api", () => {
  return {
    createUser: vi.fn(),
    authenticateAndRedirectToHome: vi.fn(),
  };
});

vi.mock("@tanstack/react-router", () => {
  return { ...mockRouterLib, useNavigate: vi.fn(() => mockNavigate) };
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

beforeEach(() => {
  renderWithQueryClient(
    <AuthContext
      value={{ currentUser: null, setCurrentUser: mockSetCurrentUser }}
    >
      <SignUpForm />
    </AuthContext>
  );

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
  const errorMsg = "error from the server";
  mockCreateUser.mockRejectedValueOnce({
    response: { data: { detail: errorMsg } },
  });
  await clickSubmitButton();
  expectErrorMessage(errorMsg);
  expect(mockSetCurrentUser).not.toHaveBeenCalled();
});
