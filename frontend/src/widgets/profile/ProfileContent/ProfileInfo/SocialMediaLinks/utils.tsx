import SocialMediaLink, { SocialMediaLinkType } from "./SocialMediaLink";

const renderSocialMediaLink = (link: SocialMediaLinkType) => {
  if (!link.href) return;

  return (
    <li key={link.title}>
      <SocialMediaLink {...link} />
    </li>
  );
};

export { renderSocialMediaLink };
