import { render, screen } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";
import ProfileArticles from ".";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
  UseQueryResult,
} from "@tanstack/react-query";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";

vi.mock("@tanstack/react-router", async () => {
  return {
    useSearch: vi.fn(() => ({ page: 1 })),
    useParams: vi.fn(() => ({ username: "test" })),
    Link: vi.fn(),
  };
});

vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual("@tanstack/react-query");
  return { ...actual, useQuery: vi.fn() };
});

const mockUseQuery = vi.mocked(useQuery, { partial: true });

const queryClient = new QueryClient();

beforeEach(() => {
  render(
    <QueryClientProvider client={queryClient}>
      <ProfileArticles />
    </QueryClientProvider>
  );
});

type UseQueryReturnType = Partial<
  UseQueryResult<ServerPaginatedArticlesResponse>
>;

const useQueryReturnValue: UseQueryReturnType = {
  data: { count: 3, results: [], page_amount: 1, next: null, previous: null },
};

// mock for ProfileArticles
mockUseQuery.mockReturnValueOnce(useQueryReturnValue);
// mock for ListOfArticles
mockUseQuery.mockReturnValueOnce(useQueryReturnValue);

test("successfully displays user articles and paginator", () => {
  const listOfArticles = screen.getByTestId("list-of-articles");
  const paginator = screen.getByTestId("paginator");
  expect(listOfArticles).toBeDefined();
  expect(paginator).toBeDefined();
});

mockUseQuery.mockReturnValueOnce({
  data: { ...useQueryReturnValue.data, count: 0 },
});

test("shows no articles message", () => {
  const msg = screen.getByTestId("user-has-no-articles-msg");
  expect(msg).toBeDefined();
});

mockUseQuery.mockReturnValueOnce({ error: new Error("404") });

test("doesn't display anything when error occurs", () => {
  const listOfArticles = screen.queryByTestId("list-of-articles");
  const paginator = screen.queryByTestId("paginator");
  expect(listOfArticles).toBeNull();
  expect(paginator).toBeNull();
});
