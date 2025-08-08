import React from "react";
import "./index.scss";

export type SocialMediaLinkType = {
  title: string;
  href: string | null;
  icon: React.JSX.Element;
};

const SocialMediaLink: React.FC<SocialMediaLinkType> = ({
  title,
  href,
  icon,
}) => {
  if (!href) return undefined;

  return (
    <a href={href} title={title} className="social-media-link">
      <div className="wrapper">{icon}</div>
    </a>
  );
};

export default SocialMediaLink;
