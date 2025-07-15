import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import PreviousPageLink from ".";
import { PaginatorContext } from "../context";

const currentPage = 5;
const router = createRouterWithRootComponent(
  <PaginatorContext value={{ currentPage, pageAmount: 10 }}>
    <PreviousPageLink />
  </PaginatorContext>
);

beforeEach(() => {
  renderWithRouting(router);
});

test("link to the previous page redirects to previous page", () => {
  const link = screen.getByText("<");
  click(link);
  expect(router.history.location.search).toContain(`page=${currentPage - 1}`);
});
