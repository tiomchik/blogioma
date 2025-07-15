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
  options?: { amount?: number; page?: number }
) => {
  const sortingField = getSortingFieldByCriteria(criteria);
  const response = await axios.get<ServerPaginatedArticlesResponse>(
    ARTICLES_BASE_URL,
    {
      params: {
        order_by: sortingField,
        page_size: options?.amount,
        page: options?.page,
      },
    }
  );
  return response.data;
};

const getSortingFieldByCriteria = (criteria: ArticleSortingCriterias) => {
  const sortingField = criteriaToSortingFieldMap[criteria];
  if (!sortingField) throw new Error("Invalid sorting criteria");
  return sortingField;
};

export { loadArticlesSortedByCriteria, getSortingFieldByCriteria };
