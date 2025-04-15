import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="container">
      <h3>Welcome Home!</h3>
    </div>
  );
}
