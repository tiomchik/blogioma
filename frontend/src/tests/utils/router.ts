import { createRootRoute, createRouter } from "@tanstack/react-router";
import { JSX } from "react";

const createRouterWithRootComponent = (rootComponent: JSX.Element) => {
  const root = createRootRoute({
    component: () => rootComponent,
  });
  return createRouter({ routeTree: root });
};

export { createRouterWithRootComponent };
