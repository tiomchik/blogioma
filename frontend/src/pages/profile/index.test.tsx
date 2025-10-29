import { test, vi } from "vitest";
import ProfilePage from ".";
import {
  renderWithAuth,
  expectElementWithTestId,
  expectNoElementWithTestId,
} from "@/tests/utils";
const { mockRouterLib, mockQueryLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

const profileOwner = { username: "user" };

vi.mock("@tanstack/react-router", () => {
  return {
    ...mockRouterLib,
    useParams: vi.fn(() => ({ username: profileOwner.username })),
    useSearch: vi.fn(() => ({ page: 1 })),
  };
});
vi.mock("@tanstack/react-query", () => mockQueryLib);

test("all components are displayed successfully", async () => {
  await renderWithAuth(<ProfilePage />, {
    currentUser: profileOwner,
  });

  expectElementWithTestId("page-heading");
  expectElementWithTestId("profile-area");
  expectElementWithTestId("profile-navigation");
  expectElementWithTestId("profile-content");
});

test("profile navigation hidden when user isn't profile owner", async () => {
  await renderWithAuth(<ProfilePage />, {
    currentUser: { username: "otherUser" },
  });
  expectNoElementWithTestId("profile-navigation");
});
