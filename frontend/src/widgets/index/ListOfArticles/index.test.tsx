import { screen } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";
import {
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import ListOfArticles from "./";
import { Article } from "@/app/types";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";

const article: Article = {
  id: 1,
  heading: "article 1",
  full_text: "full text",
  pub_date: "2023-09-01T00:00:00.000Z",
  update: "2023-09-01T00:00:00.000Z",
  author: {
    username: "testUser",
    pfp: "url/to/pfp",
  },
  viewings: 100000,
};

const articles: Article[] = [];

for (let i = 0; i <= 3; i++) {
  articles.push({
    ...article,
    heading: `article ${i}`,
    id: i,
  });
}

const queryClient = new QueryClient();

const router = createRouterWithRootComponent(
  <QueryClientProvider client={queryClient}>
    <ListOfArticles orderByField="id" />
  </QueryClientProvider>
);

beforeEach(() => {
  renderWithRouting(router);
});

vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual("@tanstack/react-query");
  return { ...actual, useQuery: vi.fn() };
});

const mockedUseQuery = vi.mocked(useQuery, { partial: true });

mockedUseQuery.mockReturnValueOnce({
  isLoading: true,
});

test("displays loading state", () => {
  const loading = screen.getByText("Loading...");
  expect(loading).toBeTruthy();
});

mockedUseQuery.mockReturnValueOnce({
  data: {
    results: articles,
  },
});

test("displays articles ordered by id", () => {
  for (let i = 0; i < 3; i++) {
    const article = screen.getByText(articles[i].heading);
    expect(article).toBeDefined();
  }
});

mockedUseQuery.mockReturnValueOnce({
  error: new Error("error"),
});

test("displays error", () => {
  const error = screen.getByText(/error/);
  expect(error).toBeDefined();
});
