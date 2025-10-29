import { expect, test, vi } from "vitest";
import IndexPage from ".";
import { screen } from "@testing-library/dom";
import { render } from "@testing-library/react";
import { expectElementWithTestId } from "@/tests/utils";
const { mockRouterLib, mockQueryLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-router", () => mockRouterLib);
vi.mock("@tanstack/react-query", () => mockQueryLib);

test("all components are displayed successfully", () => {
  render(<IndexPage />);

  expectElementWithTestId("page-heading");

  const articlesHeadings = screen.getAllByTestId("articles-heading");
  expect(articlesHeadings.length).toBe(2);

  const listsOfArticles = screen.getAllByTestId("list-of-articles");
  expect(listsOfArticles.length).toBe(2);
});
