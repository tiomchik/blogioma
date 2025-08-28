import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, test } from "vitest";
import SocialMediaLinks from ".";
import { ProfileDataContext } from "../context";
import { mockUser } from "@/tests/mocks";

const links = {
  youtube: "https://www.youtube.com/",
  tiktok: "https://tiktok.com/",
  twitch: "https://twitch.tv/",
  linkedin: "https://linkedin.com/",
};

describe("with social media links", () => {
  beforeEach(() => {
    render(
      <ProfileDataContext value={{ ...mockUser, ...links }}>
        <SocialMediaLinks />
      </ProfileDataContext>
    );
  });

  test("displays the social media links correctly", () => {
    const linkElements = screen.getAllByRole("link");
    const expectedLinksLength = Object.values(links).length;
    expect(linkElements.length).toBe(expectedLinksLength);
  });
});

describe("without social media links", () => {
  const emptyLinks = { youtube: "", tiktok: "", twitch: "", linkedin: "" };

  beforeEach(() => {
    render(
      <ProfileDataContext value={{ ...mockUser, ...emptyLinks }}>
        <SocialMediaLinks />
      </ProfileDataContext>
    );
  });

  test("the social media links aren't displayed", () => {
    const links = screen.queryAllByRole("link");
    expect(links.length).toBe(0);
  });
});
