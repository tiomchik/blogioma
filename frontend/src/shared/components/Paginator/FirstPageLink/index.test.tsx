import {
  click,
  createRouterWithRootComponent,
  renderWithRouting,
} from "@/tests/utils";
import { beforeEach, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import FirstPageLink from ".";

const router = createRouterWithRootComponent(<FirstPageLink />);

beforeEach(() => {
  renderWithRouting(router);
});

test("link to the first page redirects to first page", () => {
  const link = screen.getByText("1");
  click(link);
  expect(router.history.location.search).toContain("page=1");
});
