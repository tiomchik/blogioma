import { beforeEach, expect, test, vi } from "vitest";
import SignUpForm from "./";
import { createAndPopulateFormData } from "./utils";
import {
  clickSubmitButton,
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderWithProviders,
} from "@/tests/utils";
import {
  PASSWORD_CONFIRMATION_FIELD_LABEL,
  PASSWORD_FIELD_LABEL,
  USERNAME_FIELD_LABEL,
} from "./inputs";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthContext } from "@/app/contexts";
import { createUser } from "@/entities/user/api";
import axios from "axios";

vi.mock("@/entities/user/api", async () => {
  return {
    createUser: vi.fn(),
    obtainToken: vi.fn(() => "token"),
  };
});

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return {
    ...actual,
    useNavigate: vi.fn(() => mockedNavigate),
  };
});

const mockedNavigate = vi.fn();
const mockedSetCurrentUser = vi.fn();
const mockedCreateUser = vi.mocked(createUser);

const userData = {
  username: "username",
  password: "password",
  password1: "password",
};

beforeEach(async () => {
  await renderWithProviders(
    [
      {
        provider: AuthContext,
        props: { value: { setCurrentUser: mockedSetCurrentUser } },
      },
      {
        provider: QueryClientProvider,
        props: { client: new QueryClient() },
      },
    ],
    <SignUpForm />
  );
  pasteUserDataIntoForm(userData);
});

test("successful registration flow", async () => {
  await clickSubmitButton();
  const formData = createAndPopulateFormData(userData);
  expect(mockedCreateUser).toHaveBeenCalledWith(formData);
  expect(axios.defaults.headers.common["Authorization"]).toEqual("Token token");
  expect(mockedSetCurrentUser).toHaveBeenCalledWith({
    username: userData.username,
    pfp: null,
  });
  expect(mockedNavigate).toHaveBeenCalledWith({ to: "/" });
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

const pasteUserDataIntoForm = (userData: {
  username: string;
  password: string;
  password1: string;
}) => {
  pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, userData.username);
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, userData.password);
  pasteIntoFieldByLabelText(
    PASSWORD_CONFIRMATION_FIELD_LABEL,
    userData.password1
  );
};
