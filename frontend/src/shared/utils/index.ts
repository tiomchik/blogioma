import { useLocation } from "@tanstack/react-router";
import { AxiosError } from "axios";
import { UseFormSetError } from "react-hook-form";

const isOnPage = (url: string): boolean => {
  const location = useLocation();
  return location.pathname === url;
};

type ErrorResponse = { string: string[] | string };

const setErrorsFromResponse = (
  error: AxiosError,
  setError: UseFormSetError<any>
) => {
  const response = error.response?.data as ErrorResponse;
  const fields = Object.keys(response);

  for (let i = 0; i < fields.length; i++) {
    const field = fields[i] as keyof ErrorResponse;
    const errors = response[field];

    if (isGeneralServerError(errors)) {
      setError("root", { message: errors });
    } else if (isArrayOfServerErrors(field, errors)) {
      errors.forEach((errorMsg) => setError("root", { message: errorMsg }));
    } else if (isFieldErrors(field)) {
      errors.forEach((errorMsg) => setError(field, { message: errorMsg }));
    }
  }
};

const isGeneralServerError = (errors: string | string[]) => {
  return typeof errors === "string";
};

const isArrayOfServerErrors = (field: string, errors: string | string[]) => {
  return field === "detail" && Array.isArray(errors);
};

const isFieldErrors = (field: string) => {
  return field !== "detail";
};

export { isOnPage, setErrorsFromResponse };
