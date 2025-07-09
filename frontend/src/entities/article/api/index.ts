import axios from "axios";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";

const loadArticlesOrderedByField = async (field: string, amount?: number) => {
  const response = await axios.get<ServerPaginatedArticlesResponse>(
    `${import.meta.env.VITE_API_URL}/articles/?order_by=${field}&page_size=${amount ? amount : ""}`
  );
  return response.data;
};

export { loadArticlesOrderedByField };
