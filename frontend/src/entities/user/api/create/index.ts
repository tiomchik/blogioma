import { ServerUserResponse } from "@/entities/user/types";
import { REGISTER_URL } from "./constants";
import axios from "axios";

const createUser = async (userData: FormData) => {
  const response = await axios.post<ServerUserResponse>(REGISTER_URL, userData);
  return response;
};

export { createUser };
