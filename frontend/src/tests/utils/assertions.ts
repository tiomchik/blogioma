import { screen } from "@testing-library/dom";
import { expect } from "vitest";

const expectElementWithTestId = (testId: string) => {
  const element = screen.getByTestId(testId);
  expect(element).toBeDefined();
};

const expectNoElementWithTestId = (testId: string) => {
  const element = screen.queryByTestId(testId);
  expect(element).toBeNull();
};

export { expectElementWithTestId, expectNoElementWithTestId };
