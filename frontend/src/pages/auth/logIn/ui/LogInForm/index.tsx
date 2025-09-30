import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import { PasswordInput, UsernameInput, Button } from "@/shared/components";
import { useAuth } from "@/app/contexts";
import { setErrorsFromResponse } from "@/shared/utils";
import { authenticateAndRedirectToHome } from "@/entities/user/api";
import { useNavigate } from "@tanstack/react-router";
import { ErrorMessage } from "@hookform/error-message";
import { AxiosError } from "axios";

type FormInputs = {
  username: string;
  password: string;
};

const LogInForm: React.FC = () => {
  const methods = useForm<FormInputs>({ mode: "onBlur" });
  const { setCurrentUser } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data: FormInputs) => {
    try {
      await authenticateAndRedirectToHome(data, setCurrentUser, navigate);
    } catch (error: AxiosError | unknown) {
      setErrorsFromResponse(error as AxiosError, methods.setError);
    }
  };

  return (
    <FormProvider {...methods}>
      <form
        method="post"
        onSubmit={methods.handleSubmit(onSubmit)}
        data-testid="log-in-form"
      >
        <UsernameInput />
        <PasswordInput />
        <ErrorMessage
          name="root"
          render={({ message }) => <p className="form-err">{message}</p>}
        />
        <Button>Log in</Button>
      </form>
    </FormProvider>
  );
};

export default LogInForm;
