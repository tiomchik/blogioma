import { screen } from "@testing-library/react";
import { beforeEach, describe, expect, test } from "vitest";
import ReturnButton from ".";
import {
  click,
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
  expectNoElementWithTestId,
  expectElementWithTestId,
} from "@/tests/utils";

const router = createRouterWithRootComponent(<ReturnButton />);

test("doesn't render if user is not authenticated", async () => {
  await renderWithRoutingAndAuth(router, { currentUser: null });
  expectNoElementWithTestId("return-button");
});

describe("user authenticated", () => {
  const username = "testuser";

  beforeEach(() => {
    renderWithRoutingAndAuth(router, { currentUser: { username } });
  });

  test("successfully renders and redirects to user profile page", () => {
    const returnButton = screen.getByTestId("return-button");
    click(returnButton);
    expect(router.history.location.href).toBe(`/profile/${username}`);
  });

  test("renders the return icon", () => {
    expectElementWithTestId("return-icon");
  });
});
