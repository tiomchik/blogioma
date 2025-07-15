import ArticlesPage from "@/pages/articles";
import { createFileRoute } from "@tanstack/react-router";

export type ArticleSortingCriterias = "popular" | "latest";

type ArticleSearch = {
  sortingCriteria: ArticleSortingCriterias;
  page: number;
};

export const Route = createFileRoute("/articles")({
  component: ArticlesPage,
  validateSearch: (search): ArticleSearch => {
    return {
      sortingCriteria: search.sortingCriteria as ArticleSortingCriterias,
      page: search.page ? Number(search.page) : 1,
    };
  },
});
