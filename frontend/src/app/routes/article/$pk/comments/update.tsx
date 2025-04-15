import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$pk/comments/update")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$pk/comments/update"!</div>;
}
