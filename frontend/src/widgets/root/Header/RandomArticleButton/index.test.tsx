import { click, createRouterWithRootComponent } from "@/tests/utils";
import { RouterProvider } from "@tanstack/react-router";
import { render, screen } from "@testing-library/react";
import { expect, it, beforeEach } from "vitest";
import RandomArticleButton from "./";

const router = createRouterWithRootComponent(<RandomArticleButton />);

beforeEach(() => {
  render(<RouterProvider router={router} />);
});

it("random article button redirects to random article page", () => {
  const randomArticleButton = screen.getByRole("link");
  click(randomArticleButton);
  expect(router.history.location.pathname).toBe("/article/random");
});
