import axios from "axios";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";
import { ArticleSortingCriterias } from "@/app/routes/articles";
import { ARTICLES_URL } from "./constants";

const criteriaToSortingFieldMap = {
  popular: "-viewings",
  latest: "-pub_date",
};

const loadArticlesSortedByCriteria = async (
  criteria: ArticleSortingCriterias,
  options?: { amount?: number; page?: number }
) => {
  const sortedArticles = await getArticles(ARTICLES_URL, {
    sortingCriteria: criteria,
    ...options,
  });
  return sortedArticles;
};

const getSortingFieldByCriteria = (criteria: ArticleSortingCriterias) => {
  const sortingField = criteriaToSortingFieldMap[criteria];
  if (!sortingField) throw new Error("Invalid sorting criteria");
  return sortingField;
};

const getArticles = async (
  url: string,
  params?: {
    sortingCriteria?: ArticleSortingCriterias;
    amount?: number;
    page?: number;
  }
) => {
  const response = await axios.get<ServerPaginatedArticlesResponse>(url, {
    params: {
      order_by: getSortingFieldByCriteria(params?.sortingCriteria ?? "latest"),
      page_size: params?.amount,
      page: params?.page,
    },
  });
  return response.data;
};

export { loadArticlesSortedByCriteria, getSortingFieldByCriteria, getArticles };
