import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$pk/comments/add")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$pk/comments/add"!</div>;
}
