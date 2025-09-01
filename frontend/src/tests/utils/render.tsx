import { AuthContext } from "@/app/contexts";
import { AnyRouter, RouterProvider } from "@tanstack/react-router";
import { act, render } from "@testing-library/react";
import { ContextUser } from "@/app/contexts/auth";
import React, { ComponentType, JSX, PropsWithChildren } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

type ProvidersWithProps = {
  provider: ComponentType<any>;
  props?: { [key: string]: any };
}[];

const renderWithProviders = async (
  providers: ProvidersWithProps,
  component?: JSX.Element
): Promise<void> => {
  const AllProviders: React.FC<PropsWithChildren> = ({ children }) =>
    providers.reduceRight(
      (acc, { provider: Provider, props }) => (
        <Provider {...props}>{acc}</Provider>
      ),
      children
    );

  await act(async () => {
    render(<AllProviders>{component}</AllProviders>);
  });
};

const renderWithRouting = async (router: AnyRouter): Promise<void> => {
  await act(async () => {
    return render(<RouterProvider router={router} />);
  });
};

type AuthContextProps = {
  currentUser?: ContextUser | null;
  setCurrentUser?: CallableFunction;
};

const renderWithRoutingAndAuth = async (
  router: AnyRouter,
  authContextProps: AuthContextProps
) => {
  const { currentUser, setCurrentUser } = authContextProps;
  await act(async () => {
    render(
      <AuthContext
        value={{
          currentUser: currentUser || null,
          setCurrentUser: setCurrentUser || (() => {}),
        }}
      >
        <RouterProvider router={router} />
      </AuthContext>
    );
  });
};

const renderInputWithFormProvider = (input: JSX.Element) => {
  render(<FormProviderWrapper>{input}</FormProviderWrapper>);
};

const FormProviderWrapper: React.FC<PropsWithChildren> = ({ children }) => {
  const methods = useForm({ mode: "onBlur" });
  return <FormProvider {...methods}>{children}</FormProvider>;
};

const renderWithQueryClient = async (component: JSX.Element) => {
  await act(async () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        {component}
      </QueryClientProvider>
    );
  });
};

export {
  renderWithRouting,
  renderWithRoutingAndAuth,
  renderInputWithFormProvider,
  renderWithProviders,
  renderWithQueryClient,
};
