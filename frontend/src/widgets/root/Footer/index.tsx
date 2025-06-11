import { Link } from "@tanstack/react-router";
import React from "react";
import "./index.scss";

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer>
      <div className="container">
        <p>
          © blogioma {currentYear} -- All rights reserved ·{" "}
          <Link to="/about">About</Link> · <Link to="/feedback">Feedback</Link>{" "}
          · Email for contact:{" "}
          <span className="spoiler">
            {import.meta.env.VITE_SUPPORT_EMAIL || "Email not available"}
          </span>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
