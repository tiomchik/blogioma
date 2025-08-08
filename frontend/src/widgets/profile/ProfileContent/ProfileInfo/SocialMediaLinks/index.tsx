import YouTubeIcon from "./youtube.svg?react";
import TikTokIcon from "./tiktok.svg?react";
import TwitchIcon from "./twitch.svg?react";
import LinkedInIcon from "./linkedin.svg?react";
import React, { useMemo } from "react";
import SocialMediaLink, { SocialMediaLinkType } from "./SocialMediaLink";
import { useProfileData } from "../../context";
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
    <ul className="social-media-links">
      {linksWithTitles.map(renderSocialMediaLink)}
    </ul>
  );
};

const renderSocialMediaLink = (link: SocialMediaLinkType) => {
  return (
    <li key={link.title}>
      <SocialMediaLink {...link} />
    </li>
  );
};

export default SocialMediaLinks;
