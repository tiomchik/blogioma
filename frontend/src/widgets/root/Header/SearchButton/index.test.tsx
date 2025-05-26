import { beforeEach, expect, it } from "vitest";
import { click, createRouterWithRootComponent, renderWithRouting } from "@/tests/utils";
import { act, screen } from "@testing-library/react";
import SearchButton from "./";

const router = createRouterWithRootComponent(<SearchButton />);

beforeEach(() => {
  renderWithRouting(router);
});

it("search button redirects to search page", () => {
  const searchButton = screen.getByRole("link");
  click(searchButton);
  expect(router.history.location.pathname).toBe("/search");
});

it("search button changes color on search page", async () => {
  await act(async () => {
    router.navigate({ to: "/search" });
  });
  const searchButton = screen.getByRole("link");
  expect(searchButton.className).toContain("selected");
});
