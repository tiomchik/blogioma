import React from "react";
import { Link } from "@tanstack/react-router";
import RightArrowIcon from "./right-arrow.svg?react";
import "./index.scss";

type Props = {
  children: string;
  urlParamOrderBy: string;
};

const ArticlesHeading: React.FC<Props> = ({ children, urlParamOrderBy }) => {
  return (
    <div className="articles-heading">
      <h1>{children}</h1>
      <Link to="/article/$orderBy" params={{ orderBy: urlParamOrderBy }}>
        see all
        <div className="wrapper">
          <RightArrowIcon />
        </div>
      </Link>
    </div>
  );
};

export default ArticlesHeading;
