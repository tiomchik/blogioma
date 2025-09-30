import { screen } from "@testing-library/dom";
import { expect } from "vitest";

const expectElementWithTestId = (testId: string) => {
  const element = screen.getByTestId(testId);
  expect(element).toBeDefined();
};

export { expectElementWithTestId };
