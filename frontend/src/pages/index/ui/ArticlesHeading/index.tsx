import React from "react";
import { Link } from "@tanstack/react-router";
import RightArrowIcon from "./right-arrow.svg?react";
import { ArticleSortingCriterias } from "@/app/routes/articles";
import "./index.scss";

type Props = {
  children: string;
  seeAllSortingCriteria: ArticleSortingCriterias;
};

const ArticlesHeading: React.FC<Props> = ({
  children,
  seeAllSortingCriteria,
}) => {
  return (
    <div className="articles-heading" data-testid="articles-heading">
      <h1>{children}</h1>
      <Link to="/articles" search={{ sortingCriteria: seeAllSortingCriteria }}>
        see all
        <div className="wrapper">
          <RightArrowIcon />
        </div>
      </Link>
    </div>
  );
};

export default ArticlesHeading;
