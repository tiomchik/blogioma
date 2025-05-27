import { expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import Pfp from ".";

const testPfp = "url/to/pfp";

test("displays profile icon if user doesn't have a pfp", async () => {
  render(<Pfp pfp={null} />);
  const profileIcon = screen.getByTitle("profile icon");
  expect(profileIcon).toBeDefined();
});

test("displays user pfp", async () => {
  render(<Pfp pfp={testPfp} />);
  const pfp = screen.getByAltText("profile picture");
  expect(pfp).toBeDefined();
});
