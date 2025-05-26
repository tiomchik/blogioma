import { beforeEach, describe, expect, it } from "vitest";
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
    renderWithRoutingAndAuth(router, null);
  });

  it("sign up button redirects to sign up page", async () => {
    const signUpButton = screen.getByText("Sign up");
    click(signUpButton);
    expect(router.history.location.pathname).toBe("/auth/sign_up");
  });

  it("log in button redirects to log in page", async () => {
    const logInButton = screen.getByText("Log in");
    click(logInButton);
    expect(router.history.location.pathname).toBe("/auth/login");
  });
});

const user = { username: "test_user" };

describe("authorized user", () => {
  beforeEach(async () => {
    renderWithRoutingAndAuth(router, user);
  });

  it("displays user data", () => {
    const usernameElement = screen.getByText(user.username);
    expect(usernameElement).toBeDefined();
  });

  it("logout button redirects to log out page", async () => {
    const logOutButton = screen.getByText("Log out");
    click(logOutButton);
    expect(router.history.location.pathname).toBe("/auth/logout");
  });

  it("profile link redirects to user profile page", async () => {
    const profileLink = screen.getByText(user.username);
    click(profileLink);
    expect(router.history.location.pathname).toBe(`/profile/${user.username}`);
  });
});
