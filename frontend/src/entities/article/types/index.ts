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
