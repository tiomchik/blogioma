import { ErrorMessage } from "@hookform/error-message";
import { useFormContext } from "react-hook-form";
import React from "react";

export const USERNAME_FIELD_LABEL = "Username";

const UsernameInput: React.FC = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <>
      <p>
        <label htmlFor="username" className="form-label">
          {USERNAME_FIELD_LABEL}:{" "}
        </label>
        <input
          {...register("username", {
            required: "Username cannot be blank",
            maxLength: {
              value: 30,
              message: "Username should be less than 30 characters long",
            },
            minLength: {
              value: 4,
              message: "Username should be more than 4 characters long",
            },
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
