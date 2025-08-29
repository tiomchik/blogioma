import { Link } from "@tanstack/react-router";
import { generateListOfPagesAroundCurrent } from "./utils";
import { usePaginator } from "../context";

const ListOfPages: React.FC = () => {
  const { currentPage, pageAmount } = usePaginator();
  const pages = generateListOfPagesAroundCurrent(currentPage, pageAmount);

  return pages.map((page) => (
    <li key={page} data-testid="page-link">
      <Link to="." search={(old) => ({ ...old, page })}>
        {page}
      </Link>
    </li>
  ));
};

export default ListOfPages;
