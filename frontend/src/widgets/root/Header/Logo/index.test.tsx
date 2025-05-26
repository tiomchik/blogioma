import { beforeEach, expect, test } from "vitest";
import { act, screen } from "@testing-library/react";
import { click, createRouterWithRootComponent, renderWithRouting } from "@/tests/utils";
import Logo from "./";

const router = createRouterWithRootComponent(<Logo />);

beforeEach(() => {
  renderWithRouting(router);
});

test("logo button redirects to home page", () => {
  act(() => {
    router.navigate({ to: "/about" });
  });
  const logo = screen.getByRole("link");
  click(logo);
  expect(router.history.location.pathname).toBe("/");
});
