import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$pk/comments/delete")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$pk/comments/delete"!</div>;
}
