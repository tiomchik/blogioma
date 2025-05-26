import { beforeEach, describe, expect, it } from "vitest";
import { RenderResult, screen } from "@testing-library/react";
import {
  createRouterWithRootComponent,
  renderWithRoutingAndAuth,
} from "@/tests/utils";
import Header from ".";

const router = createRouterWithRootComponent(<Header />);

const user = { username: "test_user" };

let renderResult: RenderResult;

describe("not authorized user", () => {
  beforeEach(async () => {
    renderResult = await renderWithRoutingAndAuth(router, null);
  });

  it("add article button does not render", async () => {
    const addArticleButton = screen.queryByText("Add article");
    expect(addArticleButton).toBeNull();
  });
});

describe("authorized user", () => {
  beforeEach(async () => {
    renderResult = await renderWithRoutingAndAuth(router, user);
  });

  it("add article button renders", () => {
    const addArticleButton = screen.getByText("Add article");
    expect(addArticleButton).toBeDefined();
  });
});
