export type FormInputs = {
  username: string;
  password: string;
  password1: string;
  pfp?: FileList;
  email?: string;
};

export type ErrorResponse = {
  [field in "username" | "password" | "password1" | "pfp" | "email"]:
    | string[]
    | string;
};
