import { PageHeading } from "@/shared/components";
import { ArticlesHeading, ListOfArticles } from "@/widgets/index";
import React from "react";

const IndexPage: React.FC = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>Home</PageHeading>
        <ArticlesHeading urlSortParam="popular">
          Popular articles 🔥
        </ArticlesHeading>
        <ListOfArticles orderByField="-viewings" amount={12} />
        <ArticlesHeading urlSortParam="latest">
          Latest articles 🕒
        </ArticlesHeading>
        <ListOfArticles orderByField="-pub_date" amount={12} />
      </div>
    </main>
  );
};

export default IndexPage;
