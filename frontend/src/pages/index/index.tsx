import { PageHeading } from "@/shared/components";
import { ArticlesHeading } from "./ui";
import { ListOfArticles } from "@/entities/article/ui";
import React from "react";

const IndexPage: React.FC = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>Home</PageHeading>
        <ArticlesHeading seeAllSortingCriteria="popular">
          Popular articles 🔥
        </ArticlesHeading>
        <ListOfArticles sortingCriteria="popular" amount={12} />
        <ArticlesHeading seeAllSortingCriteria="latest">
          Latest articles 🕒
        </ArticlesHeading>
        <ListOfArticles sortingCriteria="latest" amount={12} />
      </div>
    </main>
  );
};

export default IndexPage;
