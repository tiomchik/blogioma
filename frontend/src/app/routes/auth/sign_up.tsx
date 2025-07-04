import SignUpPage from "@/pages/auth/signUp";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/auth/sign_up")({
  component: SignUpPage,
});
