import { createRootRoute, Outlet } from "@tanstack/react-router";
import { Header, Footer } from "@/widgets/root";

export const Route = createRootRoute({
  component: Root,
});

function Root() {
  return (
    <>
      <Header />
      <Outlet />
      <Footer />
    </>
  );
}
