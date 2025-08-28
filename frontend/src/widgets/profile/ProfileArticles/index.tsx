import { ServerPaginatedArticlesResponse } from "@/entities/article/types";
import { ListOfArticles } from "@/entities/article/ui";
import { getUserArticles } from "@/entities/user/api";
import { Paginator } from "@/shared/components";
import { useQuery } from "@tanstack/react-query";
import { useSearch } from "@tanstack/react-router";
import React from "react";
import { useProfileData } from "../ProfileContent/context";

const MAX_AMOUNT_OF_ARTICLES_PER_PAGE = 15;

const ProfileArticles: React.FC = () => {
  const { page } = useSearch({ from: "/profile/$username/" });
  const { username } = useProfileData();
  const { data, isLoading } = useQuery({
    queryKey: ["profileArticles", username, page],
    queryFn: () =>
      getUserArticles(username, {
        amount: MAX_AMOUNT_OF_ARTICLES_PER_PAGE,
        page,
      }),
  });

  if (isLoading) return "Loading...";

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
