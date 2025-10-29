import { test } from "vitest";
import { render } from "@testing-library/react";
import { expectElementWithTestId } from "@/tests/utils";
import AboutPage from ".";

test("all components are rendered successfully", () => {
  render(<AboutPage />);
  expectElementWithTestId("page-heading");
  expectElementWithTestId("about-page-description");
  expectElementWithTestId("links");
});
