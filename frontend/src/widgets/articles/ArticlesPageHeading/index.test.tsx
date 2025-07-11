import { render } from "@testing-library/react";
import { expect, test } from "vitest";
import ArticlesPageHeading from ".";

test("displays the correct heading with popular sorting criteria", () => {
  const { getByText } = render(
    <ArticlesPageHeading sortingCriteria="popular" />
  );
  const heading = getByText("Popular articles 🔥");
  expect(heading).toBeDefined();
});

test("displays the correct heading with latest sorting criteria", () => {
  const { getByText } = render(
    <ArticlesPageHeading sortingCriteria="latest" />
  );
  const heading = getByText("Latest articles 🕒");
  expect(heading).toBeDefined();
});
