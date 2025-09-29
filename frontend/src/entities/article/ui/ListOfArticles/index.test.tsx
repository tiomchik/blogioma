import { screen, render } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import { expectErrorMessage } from "@/tests/utils";
import ListOfArticles from "./";
import { ServerArticleResponse } from "@/entities/article/types";
import { useQuery } from "@tanstack/react-query";
import { mockArticle } from "@/tests/mocks";
const { mockRouterLib, mockQueryLib } = await vi.hoisted(() => import("@/tests/mocks"));

const articles: ServerArticleResponse[] = [];

for (let i = 0; i <= 3; i++) {
  articles.push({
    ...mockArticle,
    heading: `article ${i}`,
    id: i,
  });
}

vi.mock("@tanstack/react-query", () => mockQueryLib);
vi.mock("@tanstack/react-router", () => mockRouterLib);

const mockUseQuery = vi.mocked(useQuery, { partial: true });

describe("using useQuery", () => {
  beforeEach(() => {
    render(<ListOfArticles />);
  });

  mockUseQuery.mockReturnValueOnce({ isLoading: true });

  test("displays loading state", () => {
    const loading = screen.getByText("Loading...");
    expect(loading).toBeDefined();
  });

  mockUseQuery.mockReturnValueOnce({ data: { results: articles } });

  test("displays articles", () => {
    checkArticles();
  });

  mockUseQuery.mockReturnValueOnce({ error: new Error("error") });

  test("displays error", () => {
    expectErrorMessage(/error/);
  });
});

describe("using articles prop", () => {
  mockUseQuery.mockReturnValueOnce({ data: undefined });

  test("displays articles", () => {
    render(<ListOfArticles articles={articles} />);
    checkArticles();
  });
});

const checkArticles = () => {
  const articleCards = screen.getAllByTestId("article-card");
  expect(articleCards.length).toBe(articles.length);
};
