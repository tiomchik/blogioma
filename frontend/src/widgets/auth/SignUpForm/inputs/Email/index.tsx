import React from "react";
import { useFormContext } from "react-hook-form";
import { ErrorMessage } from "@hookform/error-message";

export const EMAIL_FIELD_LABEL = "Email (optional)";

const EmailInput: React.FC = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <>
      <p>
        <label htmlFor="email" className="form-label">
          {EMAIL_FIELD_LABEL}:{" "}
        </label>
        <input
          type="email"
          {...register("email", {
            pattern: {
              value: /^[^@]+@[^@]+\.[^@]+$/,
              message: "Email is not valid",
            },
          })}
          className="form-input"
          id="email"
          autoComplete="email"
        />
      </p>
      <ErrorMessage
        errors={errors}
        name="email"
        render={({ message }) => <p className="form-err">{message}</p>}
      />
    </>
  );
};

export default EmailInput;
