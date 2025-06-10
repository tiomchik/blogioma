import React from "react";
import "./index.scss";

type Props = {
  children: string;
};

const Button: React.FC<Props> = ({ children }) => {
  return <button>{children}</button>;
};

export default Button;
