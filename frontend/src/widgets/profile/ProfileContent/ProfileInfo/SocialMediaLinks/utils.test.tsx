import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import { renderSocialMediaLink } from "./utils";
import { SocialMediaLinkType } from "./SocialMediaLink";

const socialMediaLink = {
  href: "https://www.youtube.com/",
  title: "YouTube",
  icon: <div>YouTube Icon</div>,
};

test("renders link successfully", () => {
  renderSocialMediaLinkComponent(socialMediaLink);
  const link = screen.getByRole("link");
  expect(link).toBeDefined();
});

test("doesn't render link if href is empty", () => {
  renderSocialMediaLinkComponent({ ...socialMediaLink, href: "" });
  const link = screen.queryByRole("link");
  expect(link).toBeNull();
});

const renderSocialMediaLinkComponent = (
  socialMediaLink: SocialMediaLinkType
) => {
  const linkElement = renderSocialMediaLink(socialMediaLink);
  render(linkElement);
};
