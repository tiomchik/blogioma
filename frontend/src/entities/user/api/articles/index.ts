import axios from "axios";
import { generateUserArticlesUrl } from "./urls";
import { ServerPaginatedArticlesResponse } from "@/entities/article/types";

const getUserArticles = async (username: string) => {
  const url = generateUserArticlesUrl(username);
  const response = await axios.get<ServerPaginatedArticlesResponse>(url);
  return response.data;
};

export { getUserArticles };
