import { ArticlesPageHeading } from "@/widgets/articles";
import { Paginator } from "@/shared/components";
import { ListOfArticles } from "@/entities/article/ui";
import { useSearch } from "@tanstack/react-router";
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { loadArticlesSortedByCriteria } from "@/entities/article/api";

const MAX_AMOUNT_OF_ARTICLES_PER_PAGE = 15;

const ArticlesPage: React.FC = () => {
  const { sortingCriteria, page } = useSearch({ from: "/articles" });
  const { isLoading, data } = useQuery({
    queryKey: ["articles", sortingCriteria, page],
    queryFn: () =>
      loadArticlesSortedByCriteria(sortingCriteria, {
        amount: MAX_AMOUNT_OF_ARTICLES_PER_PAGE,
        page,
      }),
  });

  if (isLoading) return "Loading...";

  return (
    <main>
      <div className="container">
        <ArticlesPageHeading sortingCriteria={sortingCriteria} />
        <ListOfArticles articles={data?.results} />
        <Paginator page={page} pageAmount={data?.page_amount as number} />
      </div>
    </main>
  );
};

export default ArticlesPage;
