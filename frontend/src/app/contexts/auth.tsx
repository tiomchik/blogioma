import { createContext, useContext } from "react";

export type ContextUser = {
  username: string;
  pfp?: string | null;
};

export type AuthContextProps = {
  currentUser: ContextUser | null;
  setCurrentUser: CallableFunction;
};

const AuthContext = createContext<AuthContextProps>({
  currentUser: null,
  setCurrentUser: () => {},
});

const useAuth = () => useContext(AuthContext);

export { AuthContext, useAuth };
