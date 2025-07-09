import { ContextUser } from "@/app/contexts";

export type ServerArticleResponse = {
  id: number;
  heading: string;
  full_text: string;
  author: ContextUser;
  pub_date: string;
  viewings: number;
  update?: string | null;
};
