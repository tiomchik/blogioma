import { createContext, useContext } from "react";
import { ContextUser } from "@/app/types";

const AuthContext = createContext<{
  currentUser: ContextUser | null;
  setCurrentUser: CallableFunction;
}>({ currentUser: null, setCurrentUser: () => {} });

const useAuth = () => useContext(AuthContext);

export { AuthContext, useAuth };
