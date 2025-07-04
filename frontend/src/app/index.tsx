import { StrictMode, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AnyRouter, RouterProvider } from "@tanstack/react-router";
import { AuthContext } from "./contexts";
import { User } from "./types";

type Props = {
  queryClient: QueryClient;
  router: AnyRouter;
};

const App = ({ queryClient, router }: Props) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

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
