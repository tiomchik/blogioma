import { createContext, useContext } from "react";
import { User } from "@/app/types";

const AuthContext = createContext<{
  currentUser: User | null;
  setCurrentUser: CallableFunction;
}>({ currentUser: null, setCurrentUser: () => {} });

const useAuth = () => useContext(AuthContext);

export { AuthContext, useAuth };
