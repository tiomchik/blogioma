import React from "react";
import { ArticleCard } from "@/entities/article/ui";
import { ServerArticleResponse } from "@/entities/article/types";
import { loadArticlesSortedByCriteria } from "@/entities/article/api";
import { useQuery } from "@tanstack/react-query";
import "./index.scss";
import { ArticleSortingCriterias } from "@/app/routes/articles";

export type Props = {
  sortingCriteria?: ArticleSortingCriterias;
  amount?: number;
  articles?: ServerArticleResponse[];
};

const ListOfArticles: React.FC<Props> = ({
  sortingCriteria,
  amount,
  articles,
}) => {
  const { isLoading, data, error } = useQuery({
    queryKey: ["articles", sortingCriteria],
    queryFn: () =>
      loadArticlesSortedByCriteria(sortingCriteria as ArticleSortingCriterias, {
        amount,
      }),
    enabled: !articles,
  });

  if (isLoading) return "Loading...";

  if (error) return generateErrorMessage(error);

  return (
    <div className="articles">
      {data && data.results.map(renderArticleCard)}
      {articles && articles.map(renderArticleCard)}
    </div>
  );
};

const renderArticleCard = (article: ServerArticleResponse) => {
  return <ArticleCard {...article} key={article.id} />;
};

const generateErrorMessage = (error: Error): string => {
  return `An error has occurred: ${error.message}. Please, report this error to the feedback service.`;
};

export default ListOfArticles;
