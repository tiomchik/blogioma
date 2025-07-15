import { Link } from "@tanstack/react-router";
import React from "react";
import { usePaginator } from "../context";

const NextPageLink: React.FC = () => {
  const { currentPage } = usePaginator();

  return (
    <li>
      <Link to="." search={(old) => ({ ...old, page: currentPage + 1 })}>
        &#62;
      </Link>
    </li>
  );
};

export default NextPageLink;
