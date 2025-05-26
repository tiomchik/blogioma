import { createContext } from "react";
import { User } from "@/app/types";

const AuthContext = createContext<{ user: User | null }>({ user: null });

export { AuthContext };
