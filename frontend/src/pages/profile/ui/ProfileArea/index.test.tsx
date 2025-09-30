import { render } from "@testing-library/react";
import { test } from "vitest";
import ProfileArea from ".";
import { expectElementWithTestId } from "@/tests/utils";

const children = <div data-testid="children">children</div>;

test("renders children", () => {
  render(<ProfileArea>{children}</ProfileArea>);
  expectElementWithTestId("children");
});
