import { beforeEach, describe, expect, test, vi } from "vitest";
import { screen } from "@testing-library/react";
import Header from ".";
import { renderWithAuth } from "@/tests/utils";
const { mockRouterLib } = await vi.hoisted(() => import("@/tests/mocks"));

vi.mock("@tanstack/react-router", () => mockRouterLib);
vi.mock("@/shared/utils", () => ({ isOnPage: vi.fn() }));

const user = { username: "test_user" };

describe("not authorized user", () => {
  beforeEach(() => {
    renderWithAuth(<Header />, { currentUser: null });
  });

  test("add article button does not render", () => {
    const addArticleButton = screen.queryByText("Add article");
    expect(addArticleButton).toBeNull();
  });
});

describe("authorized user", () => {
  beforeEach(() => {
    renderWithAuth(<Header />, { currentUser: user });
  });

  test("add article button renders", () => {
    const addArticleButton = screen.getByText("Add article");
    expect(addArticleButton).toBeDefined();
  });
});
