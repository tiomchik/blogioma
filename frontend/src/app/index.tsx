import React, { StrictMode, useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AnyRouter, RouterProvider } from "@tanstack/react-router";
import { AuthContext, ContextUser } from "./contexts";
import {
  getUserFromCookies,
  obtainTokenFromCookies,
  setAuthTokenInAxiosHeaders,
} from "@/entities/user/api";

type Props = {
  queryClient: QueryClient;
  router: AnyRouter;
};

const App: React.FC<Props> = ({ queryClient, router }) => {
  const [currentUser, setCurrentUser] = useState<ContextUser | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      const user = await getUserFromCookies();
      if (!user) return;
      const token = obtainTokenFromCookies();
      setAuthTokenInAxiosHeaders(token);
      setCurrentUser(user);
    };

    loadUser();
  }, []);

  return (
    <StrictMode>
      <AuthContext value={{ currentUser, setCurrentUser }}>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </AuthContext>
    </StrictMode>
  );
};

export default App;
