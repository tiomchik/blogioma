import { createFileRoute } from "@tanstack/react-router";

export type ArticleSortingCriterias = "popular" | "latest";

type ArticleSearch = {
  sortingCriteria: ArticleSortingCriterias;
  page: number;
};

export const Route = createFileRoute("/articles")({
  component: RouteComponent,
  validateSearch: (search): ArticleSearch => {
    return {
      sortingCriteria: search.sortingCriteria as ArticleSortingCriterias,
      page: search.page ? Number(search.page) : 1,
    };
  },
});

function RouteComponent() {
  return <div>Hello "/articles"!</div>;
}
