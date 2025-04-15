import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/update")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/update"!</div>;
}
