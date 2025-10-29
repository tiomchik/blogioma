import ProfilePage from "@/pages/profile/$username";
import { createFileRoute, SearchSchemaInput } from "@tanstack/react-router";

type ProfileSearch = { page?: number } & SearchSchemaInput;

export const Route = createFileRoute("/profile/$username")({
  component: ProfilePage,
  validateSearch: (search: ProfileSearch) => {
    return { page: search.page ? Number(search.page) : 1 };
  },
});
