import { render } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import SocialMediaLinks from ".";
import { ProfileDataContext } from "../context";
import { mockUser } from "@/tests/mocks";
import { renderSocialMediaLink } from "./utils";

vi.mock("./utils", () => ({
  renderSocialMediaLink: vi.fn(),
}));

const mockRenderSocialMediaLink = vi.mocked(renderSocialMediaLink);

test("renderSocialMediaLink was called with correct params", () => {
  render(
    <ProfileDataContext value={{ ...mockUser }}>
      <SocialMediaLinks />
    </ProfileDataContext>
  );

  expect(mockRenderSocialMediaLink).toHaveBeenCalledWith({
    href: mockUser.youtube,
    title: "YouTube",
    icon: expect.any(Object),
  });
});
