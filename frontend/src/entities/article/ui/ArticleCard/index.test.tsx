import {
  click,
  createRouterWithRootComponent,
  expectElementWithTestId,
  renderWithRouting,
} from "@/tests/utils";
import ArticleCard from "./";
import { beforeEach, describe, expect, test } from "vitest";
import { screen } from "@testing-library/react";
import { mockArticle } from "@/tests/mocks";

describe("standard data", () => {
  const router = createRouterWithRootComponent(
    <ArticleCard {...mockArticle} />
  );

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("displays heading", () => {
    const heading = screen.getByText(mockArticle.heading);
    expect(heading).toBeDefined();
  });

  test("displays full text", () => {
    const full_text = screen.getByText(mockArticle.full_text);
    expect(full_text).toBeDefined();
  });

  test("displays an author data", () => {
    const username = screen.getByText(mockArticle.author.username);
    expect(username).toBeDefined();
    const pfp = screen.getByRole("img");
    expect(pfp).toBeDefined();
  });

  test("read button redirects to article page", () => {
    const readButton = screen.getAllByRole("link")[1];
    click(readButton);
    expect(router.history.location.pathname).toBe(`/article/${mockArticle.id}`);
  });

  test("displays publication date", () => {
    expectElementWithTestId("publication-date");
  });

  test("displays date of update", async () => {
    const router = createRouterWithRootComponent(
      <ArticleCard {...mockArticle} update="2025-03-28T05:44:13.389735Z" />
    );
    await renderWithRouting(router);
    expectElementWithTestId("date-of-update");
  });

  test("link to the author redirects to his profile", () => {
    const user = screen.getByText(mockArticle.author.username);
    click(user);
    expect(router.history.location.pathname).toBe(
      `/profile/${mockArticle.author.username}`
    );
  });
});

describe("long data", () => {
  const longArticle = {
    ...mockArticle,
    heading: "test heading".repeat(15),
    full_text: "test full text".repeat(15),
    author: {
      ...mockArticle.author,
      username: "user6".repeat(15),
    },
  };

  const router = createRouterWithRootComponent(
    <ArticleCard {...longArticle} />
  );

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("displays a fragment of a long heading", () => {
    const heading = screen.getByRole("heading");
    const isEndsWithEllipsis = heading?.textContent?.endsWith("...");
    expect(isEndsWithEllipsis).toBeTruthy();
  });

  test("displays a fragment of a long full text", () => {
    const fragment = screen.getAllByRole("paragraph")[0];
    const isEndsWithEllipsis = fragment?.textContent?.endsWith("...");
    expect(isEndsWithEllipsis).toBeTruthy();
  });

  test("displays a fragment of a long username", () => {
    const username = screen.getAllByRole("link")[0];
    const isEndsWithEllipsis = username?.textContent?.endsWith("...");
    expect(isEndsWithEllipsis).toBeTruthy();
  });
});
