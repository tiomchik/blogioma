import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import UserPfpWithUsername from ".";
import { ProfileDataContext } from "../context";
import { mockUser } from "@/tests/mocks";

test("displays the profile information", () => {
  render(
    <ProfileDataContext value={mockUser}>
      <UserPfpWithUsername />
    </ProfileDataContext>
  );

  const pfp = screen.getByTestId("pfp");
  const username = screen.getByText(mockUser.username);
  expect(pfp).toBeDefined();
  expect(username).toBeDefined();
});
