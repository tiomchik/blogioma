import {
  click,
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import ProfileNavigation from ".";
import { screen } from "@testing-library/dom";

const router = createRouterWithRootComponent(<ProfileNavigation />);
const username = "test";

beforeEach(() => {
  renderWithRoutingAndAuth(router, { currentUser: { username } });
});

test("link to the profile redirects to the profile page", () => {
  const link = screen.getByTestId("profile-link");
  click(link);
  expect(router.state.location.pathname).toBe(`/profile/${username}`);
});

test("link to the profile settings redirects to the profile settings page", () => {
  const link = screen.getByTestId("profile-settings-link");
  click(link);
  expect(router.state.location.pathname).toBe("/profile_settings");
});
