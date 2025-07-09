import { createContext, useContext } from "react";

export type ContextUser = {
  username: string;
  pfp?: string | null;
};

const AuthContext = createContext<{
  currentUser: ContextUser | null;
  setCurrentUser: CallableFunction;
}>({ currentUser: null, setCurrentUser: () => {} });

const useAuth = () => useContext(AuthContext);

export { AuthContext, useAuth };
