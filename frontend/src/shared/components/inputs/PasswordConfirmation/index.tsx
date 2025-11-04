import { ErrorMessage } from "@hookform/error-message";
import React from "react";
import { useFormContext } from "react-hook-form";
import { ERROR_BLANK, ERROR_MISMATCH } from "./errorMessages";

export const PASSWORD_CONFIRMATION_FIELD_LABEL = "Confirm password";

const PasswordConfirmationInput: React.FC = () => {
  const {
    register,
    formState: { errors },
    getValues,
  } = useFormContext();

  return (
    <>
      <p>
        <label htmlFor="password1" className="form-label">
          {PASSWORD_CONFIRMATION_FIELD_LABEL}:{" "}
        </label>
        <input
          type="password"
          {...register("password1", {
            required: ERROR_BLANK,
            validate: (value: string) =>
              value == getValues("password") || ERROR_MISMATCH,
          })}
          className="form-input"
          id="password1"
          autoComplete="new-password"
        />
      </p>
      <ErrorMessage
        errors={errors}
        name="password1"
        render={({ message }) => <p className="form-err">{message}</p>}
      />
    </>
  );
};

export default PasswordConfirmationInput;
