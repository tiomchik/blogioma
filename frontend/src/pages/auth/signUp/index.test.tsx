import { test, vi } from "vitest";
import SignUpPage from ".";
import { expectElementWithTestId } from "@/tests/utils";
import { render } from "@testing-library/react";
const { mockQueryLib, mockRouterLib } = await vi.hoisted(
  () => import("@/tests/mocks")
);

vi.mock("@tanstack/react-query", () => mockQueryLib);
vi.mock("@tanstack/react-router", () => mockRouterLib);

test("all components are displayed successfully", () => {
  render(<SignUpPage />);
  expectElementWithTestId("page-heading");
  expectElementWithTestId("sign-up-form");
});
