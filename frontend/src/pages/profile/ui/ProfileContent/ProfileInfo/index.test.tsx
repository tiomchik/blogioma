import { beforeEach, expect, test, vi } from "vitest";
import ProfileInfo from ".";
import { useQuery } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { expectElementWithTestId } from "@/tests/utils";
const { mockRouterLib, mockQueryLib, mockUser } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-router", async () => {
  return {
    ...mockRouterLib,
    useParams: vi.fn(() => ({ username: mockUser.username })),
  };
});

vi.mock("@tanstack/react-query", () => mockQueryLib);

const mockUseQuery = vi.mocked(useQuery, { partial: true });

beforeEach(() => {
  render(<ProfileInfo />);
});

mockUseQuery.mockReturnValueOnce({ data: mockUser });

test("renders the profile info successfully", () => {
  expectElementWithTestId("user-pfp-with-username");
  expectElementWithTestId("social-media-links");
});

mockUseQuery.mockReturnValueOnce({ isLoading: true });

test("renders loading state", () => {
  const loading = screen.getByText("Loading...");
  expect(loading).toBeDefined();
});

const errorMsg = "error";
mockUseQuery.mockReturnValueOnce({ error: new Error(errorMsg) });

test("renders error", () => {
  const error = screen.getByText(errorMsg);
  expect(error).toBeDefined();
});

mockUseQuery.mockReturnValueOnce({ error: new Error("404") });

test("renders 404 error", () => {
  expectElementWithTestId("not-found-msg");
});
