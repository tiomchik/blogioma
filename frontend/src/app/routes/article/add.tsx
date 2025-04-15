import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/add")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/add"!</div>;
}
