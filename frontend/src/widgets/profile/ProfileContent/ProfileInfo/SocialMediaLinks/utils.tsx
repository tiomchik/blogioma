import SocialMediaLink, { SocialMediaLinkType } from "./SocialMediaLink";

const renderSocialMediaLink = (link: SocialMediaLinkType) => {
  return (
    <li key={link.title}>
      <SocialMediaLink {...link} />
    </li>
  );
};

export { renderSocialMediaLink };
