import { ArticleSortOptions } from "@/app/routes/articles";
import { PageHeading } from "@/shared/components";

type Props = { sortingCriteria: ArticleSortOptions };

const criteriaToHeadingMap = {
  popular: "Popular articles 🔥",
  latest: "Latest articles 🕒",
};

const ArticlesPageHeading: React.FC<Props> = ({ sortingCriteria }) => {
  const heading = criteriaToHeadingMap[sortingCriteria];
  return <PageHeading>{heading}</PageHeading>;
};

export default ArticlesPageHeading;
