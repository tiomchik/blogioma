import { ContextUser } from "./auth";

export type Article = {
  id: number;
  heading: string;
  full_text: string;
  author: ContextUser;
  pub_date: string;
  viewings: number;
  update?: string | null;
};
