import { generateUserArticlesUrl } from "./urls";
import { getArticles } from "@/entities/article/api";

const getUserArticles = async (
  username: string,
  options?: { amount?: number; page?: number }
) => {
  const url = generateUserArticlesUrl(username);
  const userArticles = await getArticles(url, options);
  return userArticles;
};

export { getUserArticles };
