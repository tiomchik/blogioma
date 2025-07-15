import { ServerUserResponse } from "@/entities/user/types";

export type ServerArticleResponse = {
  id: number;
  heading: string;
  full_text: string;
  author: ServerUserResponse;
  pub_date: string;
  viewings: number;
  update?: string | null;
};

export type ServerPaginatedArticlesResponse = {
  count: number;
  page_amount: number;
  next: string | null;
  previous: string | null;
  results: ServerArticleResponse[];
};
