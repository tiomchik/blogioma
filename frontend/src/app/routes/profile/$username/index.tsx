import ProfilePage from "@/pages/profile";
import { createFileRoute } from "@tanstack/react-router";

type ProfileSearch = { page?: number }

export const Route = createFileRoute("/profile/$username/")({
  component: ProfilePage,
  validateSearch: (search: ProfileSearch) => {
    return { page: search.page ? Number(search.page) : 1 };
  },
});
