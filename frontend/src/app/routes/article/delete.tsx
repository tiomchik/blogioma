import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/delete")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/delete"!</div>;
}
