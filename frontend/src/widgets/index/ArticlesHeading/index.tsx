import React from "react";
import { Link } from "@tanstack/react-router";
import RightArrowIcon from "./right-arrow.svg?react";
import { ArticleSortOptions } from "@/app/routes/articles";
import "./index.scss";

type Props = {
  children: string;
  urlParamOrderBy: ArticleSortOptions;
};

const ArticlesHeading: React.FC<Props> = ({ children, urlParamOrderBy }) => {
  return (
    <div className="articles-heading">
      <h1>{children}</h1>
      <Link to="/articles" search={{ sort: urlParamOrderBy }}>
        see all
        <div className="wrapper">
          <RightArrowIcon />
        </div>
      </Link>
    </div>
  );
};

export default ArticlesHeading;
