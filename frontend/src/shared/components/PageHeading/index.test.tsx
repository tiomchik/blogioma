import { expect, test } from "vitest";
import PageHeading from "./";
import { render, screen } from "@testing-library/react";

test("shows text", () => {
  const text = "Test";
  render(<PageHeading>{text}</PageHeading>);
  const pageHeading = screen.getByText(text);
  expect(pageHeading).toBeDefined();
});
