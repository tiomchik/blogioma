import { createRootRoute, Outlet } from "@tanstack/react-router";
import { Header } from "@/widgets/root";

export const Route = createRootRoute({
  component: Root,
});

function Root() {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}
