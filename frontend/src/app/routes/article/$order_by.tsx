import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/article/$order_by")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/article/$order_by"!</div>;
}
