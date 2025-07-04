import { PageHeading } from "@/shared/components";
import { SignUpForm } from "@/widgets/auth";
import React from "react";

const SignUpPage: React.FC = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>Sign up</PageHeading>
        <SignUpForm />
      </div>
    </main>
  );
};

export default SignUpPage;
