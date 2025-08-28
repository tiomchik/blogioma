import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import ProfileArea from ".";

const children = <div data-testid="children">children</div>;

test("renders children", () => {
  render(<ProfileArea>{children}</ProfileArea>);
  const renderedChildren = screen.getByTestId("children");
  expect(renderedChildren).toBeDefined();
});
