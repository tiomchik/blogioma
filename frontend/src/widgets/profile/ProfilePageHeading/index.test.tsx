import { expect, test, vi } from "vitest";
import ProfilePageHeading from "./";
import { render, screen } from "@testing-library/react";

vi.mock("@tanstack/react-router", () => ({
  useParams: vi.fn(() => ({ username })), Link: vi.fn()
}));

const username = "test";

test("correctly displays username", () => {
  render(<ProfilePageHeading />);
  const heading = screen.getByText(`${username}'s profile`);
  expect(heading).toBeDefined();
});
