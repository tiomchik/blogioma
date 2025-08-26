import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, describe, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import { PaginatorContext } from "../context";
import LastPageLink from ".";

describe("pageAmount > 1", () => {
  const pageAmount = 10;
  const router = createRouterForLastPageLink(pageAmount);

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("link to the last page redirects to last page", () => {
    const link = screen.getByText(pageAmount);
    click(link);
    expect(router.history.location.search).toContain(`page=${pageAmount}`);
  });
});

describe("pageAmount == 1", () => {
  const pageAmount = 1;
  const router = createRouterForLastPageLink(pageAmount);

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("link to the last page is not displayed", () => {
    const link = screen.queryByText(pageAmount);
    expect(link).toBeNull();
  });
});

const createRouterForLastPageLink = (pageAmount: number) => {
  return createRouterWithRootComponent(
    <PaginatorContext value={{ currentPage: 1, pageAmount }}>
      <LastPageLink />
    </PaginatorContext>
  );
};
