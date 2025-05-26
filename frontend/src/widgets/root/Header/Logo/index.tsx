import React from "react";
import { Link } from "@tanstack/react-router";
import logo from "./logo.png";

const Logo: React.FC = () => {
  return (
    <Link to="/">
      <img src={logo} alt="Logo" />
    </Link>
  );
};

export default Logo;
