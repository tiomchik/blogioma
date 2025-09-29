import React from "react";
import "./index.scss";

type Props = { children: string | string[] };

const PageHeading: React.FC<Props> = ({ children }) => {
  return (
    <h1 className="page-heading" data-testid="page-heading">
      {children}
    </h1>
  );
};

export default PageHeading;
