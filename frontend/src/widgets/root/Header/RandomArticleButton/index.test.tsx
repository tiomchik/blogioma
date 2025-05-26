import { click, createRouterWithRootComponent, renderWithRouting } from "@/tests/utils";
import { screen } from "@testing-library/react";
import { expect, test, beforeEach } from "vitest";
import RandomArticleButton from "./";

const router = createRouterWithRootComponent(<RandomArticleButton />);

beforeEach(() => {
  renderWithRouting(router);
});

test("random article button redirects to random article page", () => {
  const randomArticleButton = screen.getByRole("link");
  click(randomArticleButton);
  expect(router.history.location.pathname).toBe("/article/random");
});
