import { render, screen } from "@testing-library/react";
import { beforeEach, expect, test } from "vitest";
import UserPfpWithUsername from ".";
import { ProfileDataContext } from "../../context";
import { mockUser } from "@/tests/mocks";

beforeEach(() => {
  render(
    <ProfileDataContext value={mockUser}>
      <UserPfpWithUsername />
    </ProfileDataContext>
  );
});

test("displays the profile information", () => {
  const pfp = screen.getByAltText("profile picture");
  const username = screen.getByText(mockUser.username);
  expect(pfp).toBeDefined();
  expect(username).toBeDefined();
});
