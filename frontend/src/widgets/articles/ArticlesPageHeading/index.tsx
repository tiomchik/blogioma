import { ArticleSortingCriterias } from "@/app/routes/articles";
import { PageHeading } from "@/shared/components";

type Props = { sortingCriteria: ArticleSortingCriterias };

const criteriaToHeadingMap = {
  popular: "Popular articles 🔥",
  latest: "Latest articles 🕒",
};

const ArticlesPageHeading: React.FC<Props> = ({ sortingCriteria }) => {
  const heading = criteriaToHeadingMap[sortingCriteria];
  return <PageHeading>{heading}</PageHeading>;
};

export default ArticlesPageHeading;
