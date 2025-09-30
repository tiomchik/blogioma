import { render, screen } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";
import ProfileArticles from ".";
import { useQuery, UseQueryResult } from "@tanstack/react-query";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";
import { expectElementWithTestId } from "@/tests/utils";
const { mockRouterLib, mockQueryLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-router", async () => {
  return {
    ...mockRouterLib,
    useSearch: vi.fn(() => ({ page: 1 })),
    useParams: vi.fn(() => ({ username: "test" })),
  };
});

vi.mock("@tanstack/react-query", () => mockQueryLib);

const mockUseQuery = vi.mocked(useQuery, { partial: true });

beforeEach(() => {
  render(<ProfileArticles />);
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
  expectElementWithTestId("list-of-articles");
  expectElementWithTestId("paginator");
});

mockUseQuery.mockReturnValueOnce({
  data: { ...useQueryReturnValue.data, count: 0 },
});

test("shows no articles message", () => {
  expectElementWithTestId("user-has-no-articles-msg");
});

mockUseQuery.mockReturnValueOnce({ error: new Error("404") });

test("doesn't display anything when error occurs", () => {
  const listOfArticles = screen.queryByTestId("list-of-articles");
  const paginator = screen.queryByTestId("paginator");
  expect(listOfArticles).toBeNull();
  expect(paginator).toBeNull();
});
