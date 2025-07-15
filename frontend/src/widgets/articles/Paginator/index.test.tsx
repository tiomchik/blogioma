import { screen } from "@testing-library/react";
import { beforeEach, describe, expect, test } from "vitest";
import Paginator, { Props } from ".";
import {
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";

describe("when current page is the first page", () => {
  const page = 1;
  const router = createRouterForPaginator({ page, pageAmount: 10 });

  beforeEach(() => {
    renderWithRouting(router);
  });

  test("link to the previous page is not displayed", () => {
    const link = screen.queryAllByText("<")[0];
    expect(link).not.toBeDefined();
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
    const link = screen.queryAllByText(">")[0];
    expect(link).not.toBeDefined();
  });
});

const createRouterForPaginator = (props: Props) => {
  return createRouterWithRootComponent(<Paginator {...props} />);
};
