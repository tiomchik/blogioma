import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/feedback")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/feedback"!</div>;
}
