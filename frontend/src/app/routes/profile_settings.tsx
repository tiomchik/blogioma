import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/profile_settings")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/profile_settings"!</div>;
}
