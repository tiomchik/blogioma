import { JSX, StrictMode, useState } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "@/app/styles/index.scss";

import { routeTree } from "./routeTree.gen";
import { AuthContext } from "@/app/contexts";
import { User } from "@/app/types";

const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const queryClient = new QueryClient();

const AuthWrapper = ({
  children,
  user,
}: {
  children: JSX.Element;
  user: User | null;
}): JSX.Element => {
  const [currentUser, setCurrentUser] = useState<User | null>(user);
  return (
    <AuthContext value={{ currentUser, setCurrentUser }}>
      {children}
    </AuthContext>
  );
};

const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <StrictMode>
      <AuthWrapper user={null}>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </AuthWrapper>
    </StrictMode>
  );
}
