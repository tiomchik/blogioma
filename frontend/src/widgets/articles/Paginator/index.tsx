import React from "react";
import PreviousPageLink from "./PreviousPage";
import NextPageLink from "./NextPage";
import ListOfPages from "./ListOfPages";
import FirstPageLink from "./FirstPageLink";
import LastPageLink from "./LastPageLink";
import { hasManyPagesBeforeCurrent, hasManyPagesAfterCurrent } from "./utils";
import { PaginatorContext } from "./context";
import "./index.scss";

export type Props = { page: number; pageAmount: number };

const Paginator: React.FC<Props> = ({ page, pageAmount }) => {
  return (
    <PaginatorContext value={{ currentPage: page, pageAmount }}>
      <ul className="paginator" data-testid="paginator">
        {page > 1 && <PreviousPageLink />}
        <FirstPageLink />
        {hasManyPagesBeforeCurrent(page) && <li>...</li>}
        <ListOfPages />
        {hasManyPagesAfterCurrent(page, pageAmount) && <li>...</li>}
        <LastPageLink />
        {page < pageAmount && <NextPageLink />}
      </ul>
    </PaginatorContext>
  );
};

export default Paginator;
