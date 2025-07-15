import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import ListOfPages from ".";
import { generateListOfPagesAroundCurrent } from "./utils";
import { screen } from "@testing-library/dom";
import { PaginatorContext } from "../context";

const currentPage = 5;
const pageAmount = 10;
const router = createRouterWithRootComponent(
  <PaginatorContext value={{ currentPage, pageAmount }}>
    <ListOfPages />
  </PaginatorContext>
);

beforeEach(() => {
  renderWithRouting(router);
});

test("list of pages was displayed", () => {
  const expectedPages = generateListOfPagesAroundCurrent(
    currentPage,
    pageAmount
  );
  const links = screen.getAllByRole("link").map((link) => link.textContent);
  expect(links).toEqual(expectedPages.map(String));
});

test("link with page number redirects to this page", () => {
  const expectedPage = currentPage + 1;
  const link = screen.getByText(expectedPage);
  click(link);
  expect(router.history.location.search).toContain(`page=${expectedPage}`);
});
