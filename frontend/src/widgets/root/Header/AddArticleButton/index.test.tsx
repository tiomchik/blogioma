import { test, expect, beforeEach } from "vitest";
import { act, screen } from "@testing-library/react";
import { click, createRouterWithRootComponent, renderWithRouting } from "@/tests/utils";
import AddArticleButton from "./";

const router = createRouterWithRootComponent(<AddArticleButton />);

beforeEach(() => {
  renderWithRouting(router);
});

test("add article button redirects to add article page", async () => {
  const addArticleButton = screen.getByRole("link");
  click(addArticleButton);
  expect(router.history.location.pathname).toBe("/article/add");
});

test("add article button changes color on add article page", async () => {
  await act(async () => {
    router.navigate({ to: "/article/add" });
  });
  const addArticleButton = screen.getByRole("link");
  expect(addArticleButton.className).toContain("selected");
});
