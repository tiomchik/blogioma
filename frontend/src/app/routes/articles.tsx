import { createFileRoute } from "@tanstack/react-router";

export type ArticleSortingCriterias = "popular" | "latest";

type ArticleSearch = {
  sortingCriteria: ArticleSortingCriterias;
};

export const Route = createFileRoute("/articles")({
  component: RouteComponent,
  validateSearch: (search): ArticleSearch => {
    return {
      sortingCriteria: search.sortingCriteria as ArticleSortingCriterias,
    };
  },
});

function RouteComponent() {
  return <div>Hello "/articles"!</div>;
}
