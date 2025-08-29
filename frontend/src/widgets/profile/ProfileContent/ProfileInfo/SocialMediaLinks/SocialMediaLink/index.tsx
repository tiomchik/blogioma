import React from "react";
import "./index.scss";

export type SocialMediaLinkType = {
  title: string;
  href: string;
  icon: React.JSX.Element;
};

const SocialMediaLink: React.FC<SocialMediaLinkType> = ({
  title,
  href,
  icon,
}) => {
  return (
    <a href={href} title={title} className="social-media-link">
      <div className="wrapper">{icon}</div>
    </a>
  );
};

export default SocialMediaLink;
