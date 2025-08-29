import YouTubeIcon from "./icons/youtube.svg?react";
import TikTokIcon from "./icons/tiktok.svg?react";
import TwitchIcon from "./icons/twitch.svg?react";
import LinkedInIcon from "./icons/linkedin.svg?react";
import React, { useMemo } from "react";
import { SocialMediaLinkType } from "./SocialMediaLink";
import { useProfileData } from "../context";
import { renderSocialMediaLink } from "./utils";
import "./index.scss";

const SocialMediaLinks: React.FC = () => {
  const { youtube, tiktok, twitch, linkedin } = useProfileData();

  const linksWithTitles: SocialMediaLinkType[] = useMemo(
    () => [
      { title: "YouTube", href: youtube, icon: <YouTubeIcon /> },
      { title: "TikTok", href: tiktok, icon: <TikTokIcon /> },
      { title: "Twitch", href: twitch, icon: <TwitchIcon /> },
      { title: "LinkedIn", href: linkedin, icon: <LinkedInIcon /> },
    ],
    [youtube, tiktok, twitch, linkedin]
  );

  return (
    <ul className="social-media-links" data-testid="social-media-links">
      {linksWithTitles.map((link) => renderSocialMediaLink(link))}
    </ul>
  );
};

export default SocialMediaLinks;
