import { expect, test } from "vitest";
import {
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import { screen } from "@testing-library/react";
import Account from "./";

const router = createRouterWithRootComponent(<Account />);

const user = { username: "test_user", pfp: "url/to/pfp" };

test("displays profile icon if user doesn't have a pfp", async () => {
  await renderWithRoutingAndAuth(router, null);
  const profileIcon = screen.getByTitle("profile icon");
  expect(profileIcon).toBeDefined();
});

test("displays user pfp", async () => {
  await renderWithRoutingAndAuth(router, user);
  const pfp = screen.getByAltText("profile picture");
  expect(pfp).toBeDefined();
});
