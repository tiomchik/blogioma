import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import { screen } from "@testing-library/react";
import ArticlesHeading from ".";

const text = "articles heading";
const orderBy = "viewings";
const router = createRouterWithRootComponent(
  <ArticlesHeading orderBy={orderBy}>{text}</ArticlesHeading>
);

beforeEach(() => {
  renderWithRouting(router);
});

test("shows text", () => {
  const articlesHeading = screen.getByText(text);
  expect(articlesHeading).toBeDefined();
});

test("arrow button redirects to list of ordered articles", () => {
  const arrowButton = screen.getByRole("link");
  click(arrowButton);
  expect(router.history.location.pathname).toBe(`/article/${orderBy}`);
});
