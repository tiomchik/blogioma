import { ErrorMessage } from "@hookform/error-message";
import React from "react";
import { useFormContext } from "react-hook-form";

export const PASSWORD_FIELD_LABEL = "Password";

const PasswordInput: React.FC = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <>
      <p>
        <label htmlFor="password" className="form-label">
          {PASSWORD_FIELD_LABEL}:{" "}
        </label>
        <input
          type="password"
          {...register("password", {
            required: "Password cannot be blank",
            minLength: {
              value: 8,
              message: "Password should be more than 8 characters long",
            },
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
