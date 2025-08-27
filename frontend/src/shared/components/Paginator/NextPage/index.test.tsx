import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import NextPageLink from ".";
import { PaginatorContext } from "../context";

const currentPage = 5;
const router = createRouterWithRootComponent(
  <PaginatorContext value={{ currentPage, pageAmount: 10 }}>
    <NextPageLink />
  </PaginatorContext>
);

beforeEach(() => {
  renderWithRouting(router);
});

test("link to the next page redirects to next page", () => {
  const link = screen.getByText(">");
  click(link);
  expect(router.history.location.search).toContain(`page=${currentPage + 1}`);
});
