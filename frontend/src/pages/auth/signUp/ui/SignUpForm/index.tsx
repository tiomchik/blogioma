import { useAuth } from "@/app/contexts";
import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import {
  PasswordConfirmationInput,
  PasswordInput,
  UsernameInput,
  EmailInput,
  PfpInput,
  Button,
} from "@/shared/components";
import { setErrorsFromResponse } from "@/shared/utils";
import { useMutation } from "@tanstack/react-query";
import { AxiosError, AxiosResponse } from "axios";
import { ErrorMessage } from "@hookform/error-message";
import { createUser } from "@/entities/user/api";
import { useNavigate } from "@tanstack/react-router";
import { authenticateAndRedirectToHome } from "@/entities/user/api";

type FormInputs = {
  username: string;
  password: string;
  password1: string;
  pfp?: FileList;
  email?: string;
};

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
      onSuccess: () =>
        authenticateAndRedirectToHome(data, setCurrentUser, navigate),
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

export const createAndPopulateFormData = (data: FormInputs) => {
  const formData = new FormData();
  formData.append("username", data.username);
  formData.append("password", data.password);
  formData.append("password1", data.password1);
  if (data.pfp?.item(0)) formData.append("pfp", data.pfp[0]);
  if (data.email) formData.append("email", data.email);
  return formData;
};

export default SignUpForm;
