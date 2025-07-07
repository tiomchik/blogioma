import { beforeEach, expect, test, vi } from "vitest";
import SignUpForm from "./";
import {
  createAndPopulateFormData,
  authenticateAndRedirectToHome,
} from "./utils";
import {
  clickSubmitButton,
  createRouterWithRootComponent,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithProviders,
} from "@/tests/utils";
import {
  PASSWORD_CONFIRMATION_FIELD_LABEL,
  PASSWORD_FIELD_LABEL,
  USERNAME_FIELD_LABEL,
} from "@/shared/components";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthContext } from "@/app/contexts";
import { createUser } from "@/entities/user/api";
import { RouterProvider } from "@tanstack/react-router";

vi.mock("@/entities/user/api", async () => {
  const actual = await vi.importActual("@/entities/user/api");
  return {
    ...actual,
    createUser: vi.fn(),
    obtainToken: vi.fn(() => "token"),
  };
});

vi.mock("./utils", async () => {
  const actual = await vi.importActual("./utils");
  return {
    ...actual,
    authenticateAndRedirectToHome: vi.fn(),
  };
});

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    useNavigate: vi.fn(() => mockedNavigate),
  };
});

const mockedCreateUser = vi.mocked(createUser);
const mockedAuthenticateAndRedirectToHome = vi.mocked(
  authenticateAndRedirectToHome
);
const mockedNavigate = vi.fn();
const mockedSetCurrentUser = vi.fn();

const userData = {
  username: "username",
  password: "password",
  password1: "password",
};

beforeEach(async () => {
  await renderWithProviders([
    {
      provider: AuthContext,
      props: { value: { setCurrentUser: mockedSetCurrentUser } },
    },
    {
      provider: QueryClientProvider,
      props: { client: new QueryClient() },
    },
    {
      provider: RouterProvider,
      props: { router: createRouterWithRootComponent(<SignUpForm />) },
    },
  ]);

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
  expect(mockedCreateUser).toHaveBeenCalledWith(formData);

  // We are not using expect.toHaveBeenCalledWith here, because we need to
  // check that the pfp in the `data` argument is any instance of FileList,
  // which is not achievable by calling this function.
  const args = mockedAuthenticateAndRedirectToHome.mock.calls[0];

  const data = args[0];
  expect(data.email).toBe("");
  expect(data.password).toBe(userData.password);
  expect(data.username).toBe(userData.username);
  expect(data.pfp instanceof FileList).toBe(true);

  expect(args[1]).toBe(mockedSetCurrentUser);
  expect(args[2]).toBe(mockedNavigate);
});

test("error from the server was displayed", async () => {
  mockedCreateUser.mockRejectedValueOnce({
    request: {
      response: JSON.stringify({ detail: "error from the server" }),
    },
  });
  await clickSubmitButton();
  expectErrorMessage(/error from the server/);
  expect(mockedSetCurrentUser).not.toHaveBeenCalled();
});
