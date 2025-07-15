import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import { PaginatorContext } from "../context";
import LastPageLink from ".";

const pageAmount = 10;
const router = createRouterWithRootComponent(
  <PaginatorContext value={{ currentPage: 1, pageAmount }}>
    <LastPageLink />
  </PaginatorContext>
);

beforeEach(() => {
  renderWithRouting(router);
});

test("link to the last page redirects to last page", () => {
  const link = screen.getByText(pageAmount);
  click(link);
  expect(router.history.location.search).toContain(`page=${pageAmount}`);
});
