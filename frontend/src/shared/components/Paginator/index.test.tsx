import { screen } from "@testing-library/react";
import { beforeEach, describe, expect, test } from "vitest";
import Paginator, { Props } from ".";
import {
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";

describe("when current page is the first page", () => {
  const router = createRouterForPaginator({ page: 1, pageAmount: 10 });

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("link to the previous page is not displayed", () => {
    const link = screen.queryByTestId("previous-page-link");
    expect(link).toBeNull();
  });
});

describe("when current page is middle page", () => {
  const router = createRouterForPaginator({ page: 5, pageAmount: 10 });

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("all needed links are displayed", () => {
    const expectedLinkIds = [
      "previous-page-link",
      "first-page-link",
      "last-page-link",
      "next-page-link",
    ];

    expectedLinkIds.forEach((testId) => {
      const link = screen.getByTestId(testId);
      expect(link).toBeDefined();
    });

    const listOfPages = screen.getAllByTestId("page-link");
    expect(listOfPages).toHaveLength(5);
  });
});

describe("when current page is the last page", () => {
  const pageAmount = 10;
  const page = pageAmount;
  const router = createRouterForPaginator({ page, pageAmount });

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("link to the next page is not displayed", () => {
    const link = screen.queryByTestId("next-page-link");
    expect(link).toBeNull();
  });
});

const createRouterForPaginator = (props: Props) => {
  return createRouterWithRootComponent(<Paginator {...props} />);
};
