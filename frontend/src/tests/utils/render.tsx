import { AuthContext } from "@/app/contexts";
import {
  AnyRouter,
  RouterProvider,
} from "@tanstack/react-router";
import { act, render, RenderResult } from "@testing-library/react";
import { User } from "@/app/types";

const renderWithRouting = async (router: AnyRouter): Promise<RenderResult> => {
  let renderResult!: RenderResult;
  await act(async () => {
    renderResult = render(<RouterProvider router={router} />);
  });
  return renderResult;
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

export { renderWithRouting, renderWithRoutingAndAuth };
