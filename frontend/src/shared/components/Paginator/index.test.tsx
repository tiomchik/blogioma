import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import Paginator, { Props } from ".";
import { expectElementWithTestId, expectNoElementWithTestId } from "@/tests/utils";
const { mockRouterLib } = await vi.hoisted(() => import("@/tests/mocks"));

vi.mock("@tanstack/react-router", () => mockRouterLib);

test("previous page link isn't displayed if the current page is the first page", () => {
  renderPaginator({ page: 1, pageAmount: 10 });
  expectNoElementWithTestId("previous-page-link");
});

test("all needed links are displayed if current page is middle page", () => {
  renderPaginator({ page: 5, pageAmount: 10 });

  const expectedLinkIds = [
    "previous-page-link",
    "first-page-link",
    "last-page-link",
    "next-page-link",
  ];

  expectedLinkIds.forEach((testId) => expectElementWithTestId(testId));

  const listOfPages = screen.getAllByTestId("page-link");
  expect(listOfPages).toHaveLength(5);
});

test("next page link isn't displayed if the current page is the last page", () => {
  renderPaginator({ page: 10, pageAmount: 10 });
  expectNoElementWithTestId("next-page-link");
});

const renderPaginator = (props: Props) => {
  return render(<Paginator {...props} />);
};
