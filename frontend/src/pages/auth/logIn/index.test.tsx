import { test, vi } from "vitest";
import { render } from "@testing-library/react";
import { expectElementWithTestId } from "@/tests/utils";
import LogInPage from ".";
const { mockRouterLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-router", () => mockRouterLib);

test("all components are displayed successfully", () => {
  render(<LogInPage />);
  expectElementWithTestId("page-heading")
  expectElementWithTestId("log-in-form")
});
