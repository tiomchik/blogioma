import { expect, it } from "vitest";
import PageHeading from "./";
import { render, screen } from "@testing-library/react";

it("shows text", () => {
  const text = "Test";
  render(<PageHeading>{text}</PageHeading>);
  const pageHeading = screen.getByText(text);
  expect(pageHeading).toBeDefined();
});
