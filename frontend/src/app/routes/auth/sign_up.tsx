import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/auth/sign_up")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/auth/sign_up"!</div>;
}
