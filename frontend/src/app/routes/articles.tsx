import ArticlesPage from "@/pages/articles";
import { createFileRoute, SearchSchemaInput } from "@tanstack/react-router";

export type ArticleSortingCriterias = "popular" | "latest";

type ArticleSearch = {
  sortingCriteria: ArticleSortingCriterias;
  page?: number;
} & SearchSchemaInput;

export const Route = createFileRoute("/articles")({
  component: ArticlesPage,
  validateSearch: (search: ArticleSearch) => {
    return {
      sortingCriteria: search.sortingCriteria as ArticleSortingCriterias,
      page: search.page ? Number(search.page) : 1,
    };
  },
});
