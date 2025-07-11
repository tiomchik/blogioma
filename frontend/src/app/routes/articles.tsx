import { createFileRoute } from "@tanstack/react-router";

export type ArticleSortOptions = "popular" | "latest";

type ArticleSearch = {
  sort: ArticleSortOptions;
};

export const Route = createFileRoute("/articles")({
  component: RouteComponent,
  validateSearch: (search): ArticleSearch => {
    return { sort: search.sort as ArticleSortOptions };
  },
});

function RouteComponent() {
  return <div>Hello "/articles"!</div>;
}
