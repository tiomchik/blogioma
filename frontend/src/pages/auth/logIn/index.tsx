import { PageHeading } from "@/shared/components";
import { LogInForm } from "./ui";
import React from "react";

const LogInPage: React.FC = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>Log in</PageHeading>
        <LogInForm />
      </div>
    </main>
  );
};

export default LogInPage;
