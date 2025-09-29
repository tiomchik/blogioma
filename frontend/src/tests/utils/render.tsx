import { AuthContext, AuthContextProps } from "@/app/contexts/auth";
import { AnyRouter, RouterProvider } from "@tanstack/react-router";
import { act, render } from "@testing-library/react";
import React, { JSX, PropsWithChildren } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const renderWithRouting = async (router: AnyRouter) => {
  await act(async () => {
    return render(<RouterProvider router={router} />);
  });
};

const renderWithAuth = async (
  component: JSX.Element,
  authContextProps: AuthContextProps
) => {
  await act(async () => {
    render(<AuthContext value={authContextProps}>{component}</AuthContext>);
  });
};

const renderWithRoutingAndAuth = (
  router: AnyRouter,
  authContextProps: AuthContextProps
) => {
  renderWithAuth(<RouterProvider router={router} />, authContextProps);
};

const renderInputWithFormProvider = (input: JSX.Element) => {
  render(<FormProviderWrapper>{input}</FormProviderWrapper>);
};

const FormProviderWrapper: React.FC<PropsWithChildren> = ({ children }) => {
  const methods = useForm({ mode: "onBlur" });
  return <FormProvider {...methods}>{children}</FormProvider>;
};

const renderWithQueryClient = (component: JSX.Element) => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      {component}
    </QueryClientProvider>
  );
};

export {
  renderWithRouting,
  renderWithAuth,
  renderWithRoutingAndAuth,
  renderInputWithFormProvider,
  renderWithQueryClient,
};
