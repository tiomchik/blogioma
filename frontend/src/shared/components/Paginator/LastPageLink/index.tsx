import { Link } from "@tanstack/react-router";
import React from "react";
import { usePaginator } from "../context";

const LastPageLink: React.FC = () => {
  const { pageAmount } = usePaginator();

  if (pageAmount === 1) return;

  return (
    <li data-testid="last-page-link">
      <Link to="." search={(old) => ({ ...old, page: pageAmount })}>
        {pageAmount}
      </Link>
    </li>
  );
};

export default LastPageLink;
