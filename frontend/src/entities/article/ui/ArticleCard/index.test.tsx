import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import ArticleCard from "./";
import { beforeEach, describe, expect, test } from "vitest";
import { screen } from "@testing-library/react";
import { mockUser } from "@/tests/mocks";

const article = {
  id: 7,
  heading: "test heading",
  full_text: "test full text",
  author: mockUser,
  pub_date: "2025-03-28T05:44:13.389735Z",
  update: null,
};

describe("standard data", () => {
  const router = createRouterWithRootComponent(<ArticleCard {...article} />);

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("displays heading", () => {
    const heading = screen.getByText(article.heading);
    expect(heading).toBeDefined();
  });

  test("displays full text", () => {
    const full_text = screen.getByText(article.full_text);
    expect(full_text).toBeDefined();
  });

  test("displays an author data", () => {
    const username = screen.getByText(article.author.username);
    expect(username).toBeDefined();
    const pfp = screen.getByRole("img");
    expect(pfp).toBeDefined();
  });

  test("read button redirects to article page", () => {
    const readButton = screen.getAllByRole("link")[1];
    click(readButton);
    expect(router.history.location.pathname).toBe(`/article/${article.id}`);
  });

  test("displays publication date", () => {
    const date = screen.getByText("Published: March 28, 2025, 8:44 a.m.");
    expect(date).toBeDefined();
  });

  test("displays date of update", async () => {
    const router = createRouterWithRootComponent(
      <ArticleCard {...article} update="2025-03-28T05:44:13.389735Z" />
    );
    await renderWithRouting(router);
    const date = screen.getByText("Updated: March 28, 2025, 8:44 a.m.");
    expect(date).toBeDefined();
  });

  test("link to the author redirects to his profile", () => {
    const user = screen.getByText(article.author.username);
    click(user);
    expect(router.history.location.pathname).toBe(
      `/profile/${article.author.username}`
    );
  });
});

describe("long data", () => {
  const longArticle = {
    ...article,
    heading: "test heading".repeat(15),
    full_text: "test full text".repeat(15),
    author: {
      ...article.author,
      username: "user6".repeat(15),
    },
  };

  const router = createRouterWithRootComponent(<ArticleCard {...longArticle} />);

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
