import { ErrorMessage } from "@hookform/error-message";
import { useFormContext } from "react-hook-form";
import React from "react";
import { ERROR_BLANK, ERROR_TOO_SHORT, ERROR_TOO_LONG } from "./errorMessages";

export const USERNAME_FIELD_LABEL = "Username";

type Props = { optional?: boolean };

const UsernameInput: React.FC<Props> = ({ optional = false }) => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <>
      <p data-testid="username-input">
        <label htmlFor="username" className="form-label">
          {USERNAME_FIELD_LABEL}:{" "}
        </label>
        <input
          {...register("username", {
            required: optional ? false : ERROR_BLANK,
            maxLength: { value: 30, message: ERROR_TOO_SHORT },
            minLength: { value: 4, message: ERROR_TOO_LONG },
          })}
          className="form-input"
          id="username"
          autoComplete="username"
        />
      </p>
      <ErrorMessage
        errors={errors}
        name="username"
        render={({ message }) => <p className="form-err">{message}</p>}
      />
    </>
  );
};

export default UsernameInput;
