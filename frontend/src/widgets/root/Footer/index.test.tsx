import { expect, test, beforeEach } from "vitest";
import Footer from "./";
import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { screen } from "@testing-library/react";

const router = createRouterWithRootComponent(<Footer />);

beforeEach(() => {
  renderWithRouting(router);
});

test("have right text", () => {
  const currentYear = new Date().getFullYear();
  const regex = new RegExp(`© blogioma ${currentYear} -- All rights reserved`);
  const rights = screen.getByText(regex);
  expect(rights).toBeDefined();
});

test("link to about page redirects to about page", () => {
  const link = screen.getByText(/About/);
  click(link);
  expect(router.history.location.pathname).toBe("/about");
});

test("link to feedback page redirects to feedback page", () => {
  const link = screen.getByText(/Feedback/);
  click(link);
  expect(router.history.location.pathname).toBe("/feedback");
});

test("displays support email", () => {
  const email = screen.getByText(
    import.meta.env.VITE_SUPPORT_EMAIL || "Email not available"
  );
  expect(email).toBeDefined();
});
