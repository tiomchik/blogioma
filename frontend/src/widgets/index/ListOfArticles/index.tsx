import React from "react";
import { ArticleCard } from "@/entities/article/ui";
import { loadArticlesOrderedByField } from "@/entities/article/api";
import { Article } from "@/app/types";
import { useQuery, UseQueryResult } from "@tanstack/react-query";
import "./index.scss";

type Props = {
  orderByField: string;
  amount?: number;
};

type Response = {
  results: Article[];
};

const ListOfArticles: React.FC<Props> = ({ orderByField, amount }) => {
  const { isLoading, data, error }: UseQueryResult<Response> = useQuery({
    queryKey: ["articles"],
    queryFn: () => loadArticlesOrderedByField(orderByField, amount),
  });

  if (isLoading) return "Loading...";

  if (error) return generateErrorMessage(error);

  return (
    <div className="articles">
      <div className="container">
        {data?.results.map((article) => (
          <ArticleCard {...article} key={article.id} />
        ))}
      </div>
    </div>
  );
};

const generateErrorMessage = (error: Error): string => {
  return `An error has occurred: ${error.message}. Please, report this error to the feedback service.`;
};

export default ListOfArticles;
