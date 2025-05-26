import { RouterProvider } from "@tanstack/react-router";
import { beforeEach, expect, it } from "vitest";
import { act, render, screen } from "@testing-library/react";
import { click, createRouterWithRootComponent } from "@/tests/utils";
import Logo from "./";

const router = createRouterWithRootComponent(<Logo />);

beforeEach(() => {
  render(<RouterProvider router={router} />);
});

it("logo button redirects to home page", () => {
  act(() => {
    router.navigate({ to: "/about" });
  });
  const logo = screen.getByRole("link");
  click(logo);
  expect(router.history.location.pathname).toBe("/");
});
