import { expect, test } from "vitest";
import SocialMediaLink, { SocialMediaLinkType } from ".";
import { render, screen } from "@testing-library/react";

const link: SocialMediaLinkType = {
  title: "YouTube",
  href: "https://www.youtube.com/",
  icon: <div>YouTube Icon</div>,
};

test("displays the social media link correctly", () => {
  render(<SocialMediaLink {...link} />);
  const linkElement = screen.getByTitle(link.title);
  expect(linkElement.getAttribute("href")).toEqual(link.href);
});

test("doesn't display the social media link if the href is null", () => {
  render(<SocialMediaLink {...link} href={null} />);
  const linkElement = screen.queryByTitle(link.title);
  expect(linkElement).toBeNull();
});
