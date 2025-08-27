import { createContext, useContext } from "react";

const PaginatorContext = createContext({ currentPage: 1, pageAmount: 10 });
const usePaginator = () => useContext(PaginatorContext);

export { PaginatorContext, usePaginator };
