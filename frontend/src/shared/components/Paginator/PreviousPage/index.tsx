import { Link } from "@tanstack/react-router";
import React from "react";
import { usePaginator } from "../context";

const PreviousPageLink: React.FC = () => {
  const { currentPage } = usePaginator();

  return (
    <li data-testid="previous-page-link">
      <Link to="." search={(old) => ({ ...old, page: currentPage - 1 })}>
        &#60;
      </Link>
    </li>
  );
};

export default PreviousPageLink;
