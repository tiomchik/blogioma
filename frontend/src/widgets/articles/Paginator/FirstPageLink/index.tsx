import { Link } from "@tanstack/react-router";
import React from "react";

const FirstPageLink: React.FC = () => {
  return (
    <li>
      <Link to="." search={(old) => ({ ...old, page: 1 })}>
        1
      </Link>
    </li>
  );
};

export default FirstPageLink;
