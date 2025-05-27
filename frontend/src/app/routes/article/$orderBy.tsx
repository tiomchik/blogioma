import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$orderBy")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$orderBy"!</div>;
}
