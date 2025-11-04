import { ErrorMessage } from "@hookform/error-message";
import React from "react";
import { useFormContext } from "react-hook-form";
import { ERROR_BLANK, ERROR_TOO_SHORT } from "./errorMessages";

export const PASSWORD_FIELD_LABEL = "Password";

type Props = { optional?: boolean };

const PasswordInput: React.FC<Props> = ({ optional = false }) => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <>
      <p data-testid="password-input">
        <label htmlFor="password" className="form-label">
          {PASSWORD_FIELD_LABEL}:{" "}
        </label>
        <input
          type="password"
          {...register("password", {
            required: optional ? false : ERROR_BLANK,
            minLength: { value: 8, message: ERROR_TOO_SHORT },
          })}
          className="form-input"
          id="password"
          autoComplete="new-password"
        />
      </p>
      <ErrorMessage
        errors={errors}
        name="password"
        render={({ message }) => <p className="form-err">{message}</p>}
      />
    </>
  );
};

export default PasswordInput;
