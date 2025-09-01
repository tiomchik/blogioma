import { AuthContext, ContextUser } from "@/app/contexts/auth";
import { AnyRouter, RouterProvider } from "@tanstack/react-router";
import { act, render } from "@testing-library/react";
import React, { JSX, PropsWithChildren } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

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

const renderWithQueryClient = (component: JSX.Element) => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      {component}
    </QueryClientProvider>
  );
};

export {
  renderWithRouting,
  renderWithRoutingAndAuth,
  renderInputWithFormProvider,
  renderWithQueryClient,
};
