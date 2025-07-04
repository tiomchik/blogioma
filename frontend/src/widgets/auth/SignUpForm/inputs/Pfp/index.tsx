import { ErrorMessage } from "@hookform/error-message";
import React from "react";
import { useFormContext } from "react-hook-form";

const PfpInput: React.FC = () => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  const validate = (fileList: FileList) => {
    const pfp = fileList[0];
    if (pfp) return pfp.type.startsWith("image/") || "File is not an image";
    if (!pfp) return undefined;
  };

  return (
    <>
      <p>
        <label htmlFor="pfp" className="form-label">
          Profile picture (optional):{" "}
        </label>
        <input
          type="file"
          {...register("pfp", { validate })}
          className="form-input"
          id="pfp"
        />
      </p>
      <ErrorMessage
        errors={errors}
        name="pfp"
        render={({ message }) => <p className="form-err">{message}</p>}
      />
    </>
  );
};

export default PfpInput;
