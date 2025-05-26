import { expect, it } from "vitest";
import {
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import { screen } from "@testing-library/react";
import Account from "./";

const router = createRouterWithRootComponent(<Account />);

const user = { username: "test_user", pfp: "url/to/pfp" };

it("displays profile icon if user doesn't have a pfp", async () => {
  await renderWithRoutingAndAuth(router, null);
  const profileIcon = screen.getByTitle("profile icon");
  expect(profileIcon).toBeDefined();
});

it("displays user pfp", async () => {
  await renderWithRoutingAndAuth(router, user);
  const pfp = screen.getByAltText("profile picture");
  expect(pfp).toBeDefined();
});
