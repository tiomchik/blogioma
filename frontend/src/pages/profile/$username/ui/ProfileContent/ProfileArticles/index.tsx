import { ServerPaginatedArticlesResponse } from "@/entities/article/types";
import { ListOfArticles } from "@/entities/article/ui";
import { getUserArticles } from "@/entities/user/api";
import { Paginator } from "@/shared/components";
import { useQuery } from "@tanstack/react-query";
import { useParams, useSearch } from "@tanstack/react-router";
import React from "react";

const MAX_AMOUNT_OF_ARTICLES_PER_PAGE = 12;

const ProfileArticles: React.FC = () => {
  const { page } = useSearch({ from: "/profile/$username" });
  const { username } = useParams({ from: "/profile/$username" });
  const { data, isLoading, error } = useQuery({
    queryKey: ["profileArticles", username, page],
    queryFn: () =>
      getUserArticles(username, {
        amount: MAX_AMOUNT_OF_ARTICLES_PER_PAGE,
        page,
      }),
  });

  // The ProfileInfo component will show messages about these states,
  // that's why it's not done here.
  if (error || isLoading) return;

  return (
    <>
      <h1>User's articles:</h1>
      {isUserHasArticles(data) ? (
        <>
          <ListOfArticles amount={12} articles={data?.results} />
          <Paginator page={page} pageAmount={data?.page_amount as number} />
        </>
      ) : (
        <NoArticlesMessage />
      )}
    </>
  );
};

const NoArticlesMessage: React.FC = () => {
  return (
    <h2 data-testid="user-has-no-articles-msg">
      This user doesn't have any published articles yet
    </h2>
  );
};

const isUserHasArticles = (data?: ServerPaginatedArticlesResponse) => {
  return data?.count != 0;
};

export default ProfileArticles;
