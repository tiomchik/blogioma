import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/random")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/random"!</div>;
}
