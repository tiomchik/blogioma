import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import { renderSocialMediaLink } from "./utils";

const socialMediaLink = {
  href: "https://www.youtube.com/",
  title: "YouTube",
  icon: <div>YouTube Icon</div>,
};
const linkElement = renderSocialMediaLink(socialMediaLink);

test("renders link successfully", () => {
  render(linkElement);
  const link = screen.getByRole("link");
  expect(link).toBeDefined();
});
