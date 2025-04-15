import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$pk/report")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$pk/report"!</div>;
}
