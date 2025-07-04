import { useAuth } from "@/app/contexts";
import { Button } from "@/shared/components";
import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import {
  PasswordConfirmationInput,
  PasswordInput,
  UsernameInput,
  EmailInput,
  PfpInput,
} from "@/shared/components";
import { useMutation } from "@tanstack/react-query";
import { AxiosError, AxiosResponse } from "axios";
import { ErrorMessage } from "@hookform/error-message";
import { createUser } from "@/entities/user/api";
import { useNavigate } from "@tanstack/react-router";
import { FormInputs } from "./types";
import {
  createAndPopulateFormData,
  handleOnSuccess,
  setErrorsFromResponse,
} from "./utils";

const SignUpForm: React.FC = () => {
  const mutation = useMutation<AxiosResponse, AxiosError, FormData>({
    mutationFn: createUser,
  });
  const navigate = useNavigate();
  const methods = useForm<FormInputs>({ mode: "onBlur" });
  const { setCurrentUser } = useAuth();

  const onSubmit = (data: FormInputs) => {
    const formData = createAndPopulateFormData(data);

    mutation.mutate(formData, {
      onSuccess: () => handleOnSuccess(data, setCurrentUser, navigate),
      onError: (error) => setErrorsFromResponse(error, methods.setError),
    });
  };

  return (
    <FormProvider {...methods}>
      <form
        method="post"
        encType="multipart/form-data"
        onSubmit={methods.handleSubmit(onSubmit)}
      >
        <UsernameInput />
        <PasswordInput />
        <PasswordConfirmationInput />
        <EmailInput />
        <PfpInput />
        <ErrorMessage
          name="root"
          render={({ message }) => <p className="form-err">{message}</p>}
        />

        <Button>Sign up</Button>
        <h3>All fields can be changed in the settings.</h3>
      </form>
    </FormProvider>
  );
};

export default SignUpForm;
