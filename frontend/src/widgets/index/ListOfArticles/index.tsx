import React from "react";
import Article from "./Article";
import { Article as ArticleType } from "@/app/types";
import { useQuery, UseQueryResult } from "@tanstack/react-query";
import "./index.scss";

type Props = {
  orderByField: string;
  amount?: number;
};

type Response = {
  results: ArticleType[];
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
      {data?.results.map((article) => (
        <Article {...article} key={article.id} />
      ))}
    </div>
  );
};

const loadArticlesOrderedByField = async (
  field: string,
  amount?: number
): Promise<Response> => {
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/articles/?order_by=${field}&page_size=${amount ? amount : ""}`
  );
  return response.json();
};

const generateErrorMessage = (error: Error): string => {
  return `An error has occurred: ${error.message}. Please, report this error to the feedback service.`;
};

export default ListOfArticles;
