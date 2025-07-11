import axios from "axios";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";
import { ArticleSortingCriterias } from "@/app/routes/articles";
import { ARTICLES_BASE_URL } from "./constants";

const criteriaToSortingFieldMap = {
  popular: "-viewings",
  latest: "-pub_date",
};

const loadArticlesSortedByCriteria = async (
  criteria: ArticleSortingCriterias,
  amount?: number
) => {
  const sortingField = getSortingFieldByCriteria(criteria);
  const response = await axios.get<ServerPaginatedArticlesResponse>(
    `${ARTICLES_BASE_URL}/?order_by=${sortingField}&page_size=${amount || ""}`
  );
  return response.data;
};

const getSortingFieldByCriteria = (criteria: ArticleSortingCriterias) => {
  const sortingField = criteriaToSortingFieldMap[criteria];
  if (!sortingField) throw new Error("Invalid sorting criteria");
  return sortingField;
};

export { loadArticlesSortedByCriteria, getSortingFieldByCriteria };
