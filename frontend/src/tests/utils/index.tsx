import { AuthContext } from "@/app/contexts";
import {
  AnyRouter,
  createRootRoute,
  createRouter,
  RouterProvider,
} from "@tanstack/react-router";
import { act, render, RenderResult } from "@testing-library/react";
import { User } from "@/app/types";
import { JSX } from "react";

const createRouterWithRootComponent = (rootComponent: JSX.Element) => {
  const root = createRootRoute({
    component: () => rootComponent,
  });
  return createRouter({ routeTree: root });
};

const click = async (button: HTMLElement) => {
  await act(async () => {
    button.click();
  });
};

const renderWithRoutingAndAuth = async (
  router: AnyRouter,
  user: User | null = null
): Promise<RenderResult> => {
  let renderResult!: RenderResult;
  await act(async () => {
    renderResult = render(
      <AuthContext value={{ user }}>
        <RouterProvider router={router} />
      </AuthContext>
    );
  });
  return renderResult;
};

export { createRouterWithRootComponent, click, renderWithRoutingAndAuth };
