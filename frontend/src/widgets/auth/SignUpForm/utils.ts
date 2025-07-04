import { AxiosError } from "axios";
import { ErrorResponse, FormInputs } from "./types";
import { UseNavigateResult } from "@tanstack/react-router";
import { UseFormSetError } from "react-hook-form";
import { obtainToken, setAuthToken } from "@/entities/user/api";

export const createAndPopulateFormData = (data: FormInputs) => {
  const formData = new FormData();
  formData.append("username", data.username);
  formData.append("password", data.password);
  formData.append("password1", data.password1);
  if (data.pfp?.item(0)) formData.append("pfp", data.pfp[0]);
  if (data.email) formData.append("email", data.email);
  return formData;
};

export const handleOnSuccess = async (
  data: FormInputs,
  setCurrentUser: CallableFunction,
  navigate: UseNavigateResult<string>
) => {
  const token = await obtainToken(data.username, data.password);
  setAuthToken(token);

  setCurrentUser({
    username: data.username,
    pfp: data.pfp?.item(0),
  });

  navigate({ to: "/" });
};

export const setErrorsFromResponse = (
  error: AxiosError,
  setError: UseFormSetError<FormInputs>
) => {
  const response: ErrorResponse = JSON.parse(error.request.response);
  const fields = Object.keys(response);

  for (let i = 0; i < fields.length; i++) {
    const field = fields[i] as keyof FormInputs;
    const errors = response[field];

    // If the errors is a string,
    // then this is one general error message from the server.
    // E.g. {"detail": "Method 'GET' not allowed."}
    if (typeof errors === "string") {
      setError("root", { message: errors });
    } else {
      errors.forEach((errorMsg) => setError(field, { message: errorMsg }));
    }
  }
};
