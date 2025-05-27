import { beforeEach, describe, expect, test } from "vitest";
import { screen } from "@testing-library/react";
import {
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import Header from ".";

const router = createRouterWithRootComponent(<Header />);

const user = { username: "test_user" };

describe("not authorized user", () => {
  beforeEach(() => {
    renderWithRoutingAndAuth(router, null);
  });

  test("add article button does not render", async () => {
    const addArticleButton = screen.queryByText("Add article");
    expect(addArticleButton).toBeNull();
  });
});

describe("authorized user", () => {
  beforeEach(() => {
    renderWithRoutingAndAuth(router, user);
  });

  test("add article button renders", () => {
    const addArticleButton = screen.getByText("Add article");
    expect(addArticleButton).toBeDefined();
  });
});
