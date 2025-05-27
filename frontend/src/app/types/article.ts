import { User } from "./auth";

export type Article = {
  id: number;
  heading: string;
  full_text: string;
  author: User;
  pub_date: string;
  viewings: number;
  update?: string | null;
};
