import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import UserPfpWithUsername from ".";
import { ProfileDataContext } from "../context";
import { mockUser } from "@/tests/mocks";
import { expectElementWithTestId } from "@/tests/utils";

test("displays the profile information", () => {
  render(
    <ProfileDataContext value={mockUser}>
      <UserPfpWithUsername />
    </ProfileDataContext>
  );

  expectElementWithTestId("pfp");
  const username = screen.getByText(mockUser.username);
  expect(username).toBeDefined();
});
