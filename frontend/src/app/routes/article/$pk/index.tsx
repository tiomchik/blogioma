import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$pk/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$pk/"!</div>;
}
