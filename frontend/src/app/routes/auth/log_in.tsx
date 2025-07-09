import { createFileRoute } from "@tanstack/react-router";
import LogInPage from "@/pages/auth/logIn";

export const Route = createFileRoute("/auth/log_in")({
  component: LogInPage,
});
