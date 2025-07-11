import { PageHeading } from "@/shared/components";
import { ArticlesHeading } from "@/widgets/index";
import { ListOfArticles } from "@/entities/article/ui";
import React from "react";

const IndexPage: React.FC = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>Home</PageHeading>
        <ArticlesHeading urlSortParam="popular">
          Popular articles 🔥
        </ArticlesHeading>
        <ListOfArticles sortingCriteria="popular" amount={12} />
        <ArticlesHeading urlSortParam="latest">
          Latest articles 🕒
        </ArticlesHeading>
        <ListOfArticles sortingCriteria="latest" amount={12} />
      </div>
    </main>
  );
};

export default IndexPage;
