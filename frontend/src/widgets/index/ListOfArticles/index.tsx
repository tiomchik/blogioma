import React from "react";
import { ArticleCard } from "@/entities/article/ui";
import { loadArticlesOrderedByField } from "@/entities/article/api";
import { useQuery } from "@tanstack/react-query";
import "./index.scss";

type Props = { orderByField: string; amount?: number };

const ListOfArticles: React.FC<Props> = ({ orderByField, amount }) => {
  const { isLoading, data, error } = useQuery({
    queryKey: ["articles", orderByField],
    queryFn: () => loadArticlesOrderedByField(orderByField, amount),
  });

  if (isLoading) return "Loading...";

  if (error) return generateErrorMessage(error);

  return (
    <div className="articles">
      {data?.results.map((article) => (
        <ArticleCard {...article} key={article.id} />
      ))}
    </div>
  );
};

const generateErrorMessage = (error: Error): string => {
  return `An error has occurred: ${error.message}. Please, report this error to the feedback service.`;
};

export default ListOfArticles;
