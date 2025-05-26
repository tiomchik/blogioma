import { it, expect, beforeEach } from "vitest";
import { act, render, screen } from "@testing-library/react";
import { RouterProvider } from "@tanstack/react-router";
import { click, createRouterWithRootComponent } from "@/tests/utils";
import AddArticleButton from "./";

const router = createRouterWithRootComponent(<AddArticleButton />);

beforeEach(() => {
  render(<RouterProvider router={router} />);
});

it("add article button redirects to add article page", async () => {
  const addArticleButton = screen.getByRole("link");
  click(addArticleButton);
  expect(router.history.location.pathname).toBe("/article/add");
});

it("add article button changes color on add article page", async () => {
  await act(async () => {
    router.navigate({ to: "/article/add" });
  });
  const addArticleButton = screen.getByRole("link");
  expect(addArticleButton.className).toContain("selected");
});
