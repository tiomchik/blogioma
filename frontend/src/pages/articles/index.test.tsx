import { beforeEach, expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ArticlesPage from ".";
import { useQuery } from "@tanstack/react-query";
import { expectElementWithTestId } from "@/tests/utils";
const { mockRouterLib, mockQueryLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-router", () => {
  return {
    ...mockRouterLib,
    useSearch: vi.fn(() => ({ sortingCriteria: "latest", page: 1 })),
  };
});
vi.mock("@tanstack/react-query", () => mockQueryLib);

beforeEach(() => {
  render(<ArticlesPage />);
});

vi.mocked(useQuery, { partial: true }).mockReturnValueOnce({ isLoading: true });

test("loading state is displayed", () => {
  const loading = screen.getByText("Loading...");
  expect(loading).toBeDefined();
});

test("all components are displayed successfully", () => {
  expectElementWithTestId("page-heading");
  expectElementWithTestId("list-of-articles");
  expectElementWithTestId("paginator");
});
