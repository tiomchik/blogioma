import { beforeEach, describe, expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Header from ".";
import { AuthContext, ContextUser } from "@/app/contexts";
const { mockRouterLib } = await vi.hoisted(() => import("@/tests/mocks"));

vi.mock("@tanstack/react-router", () => mockRouterLib)
vi.mock("@/shared/utils", () => ({ isOnPage: vi.fn() }));

const user = { username: "test_user" };

describe("not authorized user", () => {
  beforeEach(() => {
    renderHeaderWithCurrentUser(null)
  });

  test("add article button does not render", () => {
    const addArticleButton = screen.queryByText("Add article");
    expect(addArticleButton).toBeNull();
  });
});

describe("authorized user", () => {
  beforeEach(() => {
    renderHeaderWithCurrentUser(user);
  });

  test("add article button renders", () => {
    const addArticleButton = screen.getByText("Add article");
    expect(addArticleButton).toBeDefined();
  });
});

const renderHeaderWithCurrentUser = (currentUser: ContextUser | null) => {
  render(
    <AuthContext value={{ currentUser, setCurrentUser: () => {} }}>
      <Header />
    </AuthContext>
  );
};
