import { beforeEach, describe, expect, test, vi } from "vitest";
import {
  createRouterWithRootComponent,
  click,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import { screen } from "@testing-library/react";
import Account from "./";
import { logOut } from "@/entities/user/api";

vi.mock("@/entities/user/api", () => {
  return { logOut: vi.fn() };
});

vi.mock("@tanstack/react-router", async () => {
  const actual = await vi.importActual("@tanstack/react-router");
  return { ...actual, useNavigate: vi.fn(() => mockedNavigate) };
});

const mockedLogOut = vi.mocked(logOut);
const mockedNavigate = vi.fn();

const router = createRouterWithRootComponent(<Account />);

describe("not authorized user", () => {
  beforeEach(() => {
    renderWithRoutingAndAuth(router, { currentUser: null });
  });

  test("sign up button redirects to sign up page", () => {
    const signUpButton = screen.getByText("Sign up");
    click(signUpButton);
    expect(router.history.location.pathname).toBe("/auth/sign_up");
  });

  test("log in button redirects to log in page", () => {
    const logInButton = screen.getByText("Log in");
    click(logInButton);
    expect(router.history.location.pathname).toBe("/auth/log_in");
  });
});

const user = { username: "test_user" };

describe("authorized user", () => {
  beforeEach(() => {
    renderWithRoutingAndAuth(router, { currentUser: user });
  });

  test("displays user data", () => {
    const usernameElement = screen.getByText(user.username);
    expect(usernameElement).toBeDefined();
  });

  test("logout button calls logOut function and refreshes the page", () => {
    const logOutButton = screen.getByText("Log out");
    click(logOutButton);
    expect(mockedLogOut).toBeCalled();
    expect(mockedNavigate).toBeCalledWith({ reloadDocument: true });
  });

  test("profile link redirects to user profile page", () => {
    const profileLink = screen.getByText(user.username);
    click(profileLink);
    expect(router.history.location.pathname).toBe(`/profile/${user.username}`);
  });
});
