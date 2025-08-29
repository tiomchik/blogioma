import { beforeEach, expect, test, vi } from "vitest";
import ProfileInfo from ".";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { mockUser } from "@/tests/mocks";

vi.mock("@tanstack/react-router", async () => {
  return {
    useParams: vi.fn(() => ({ username: mockUser.username })),
    Link: vi.fn(),
  };
});

vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual("@tanstack/react-query");
  return { ...actual, useQuery: vi.fn() };
});

const mockUseQuery = vi.mocked(useQuery, { partial: true });

beforeEach(() => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <ProfileInfo />
    </QueryClientProvider>
  );
});

mockUseQuery.mockReturnValueOnce({ isLoading: false, data: mockUser });

test("renders the profile info successfully", () => {
  const userPfpWithUsername = screen.getByTestId("user-pfp-with-username");
  const socialMediaLinks = screen.getByTestId("social-media-links");
  expect(userPfpWithUsername).toBeDefined();
  expect(socialMediaLinks).toBeDefined();
});

mockUseQuery.mockReturnValueOnce({ isLoading: true });

test("renders loading state", () => {
  const loading = screen.getByText("Loading...");
  expect(loading).toBeDefined();
});

const errorMsg = "error"
mockUseQuery.mockReturnValueOnce({ error: new Error(errorMsg) });

test("renders error", () => {
  const error = screen.getByText(errorMsg);
  expect(error).toBeDefined();
})

mockUseQuery.mockReturnValueOnce({ error: new Error("404") });

test("renders 404 error", () => {
  const error = screen.getByTestId("not-found-msg");
  expect(error).toBeDefined()
})
