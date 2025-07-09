import { beforeEach, describe, expect, test } from "vitest";
import {
  createRouterWithRootComponent,
  click,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import { screen } from "@testing-library/react";
import Account from "./";

const router = createRouterWithRootComponent(<Account />);

describe("not authorized user", () => {
  beforeEach(() => {
    renderWithRoutingAndAuth(router, { currentUser: null });
  });

  test("sign up button redirects to sign up page", async () => {
    const signUpButton = screen.getByText("Sign up");
    click(signUpButton);
    expect(router.history.location.pathname).toBe("/auth/sign_up");
  });

  test("log in button redirects to log in page", async () => {
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

  test("logout button redirects to log out page", async () => {
    const logOutButton = screen.getByText("Log out");
    click(logOutButton);
    expect(router.history.location.pathname).toBe("/auth/logout");
  });

  test("profile link redirects to user profile page", async () => {
    const profileLink = screen.getByText(user.username);
    click(profileLink);
    expect(router.history.location.pathname).toBe(`/profile/${user.username}`);
  });
});
