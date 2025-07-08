import { AxiosError } from "axios";
import { ErrorResponse, FormInputs } from "./types";
import { UseFormSetError } from "react-hook-form";

export const createAndPopulateFormData = (data: FormInputs) => {
  const formData = new FormData();
  formData.append("username", data.username);
  formData.append("password", data.password);
  formData.append("password1", data.password1);
  if (data.pfp?.item(0)) formData.append("pfp", data.pfp[0]);
  if (data.email) formData.append("email", data.email);
  return formData;
};

export const setErrorsFromResponse = (
  error: AxiosError,
  setError: UseFormSetError<FormInputs>
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

const isArrayOfServerErrors = (
  field: keyof ErrorResponse,
  errors: string | string[]
) => {
  return field === "detail" && Array.isArray(errors);
};

const isFieldErrors = (field: keyof ErrorResponse) => {
  return field !== "detail";
};
