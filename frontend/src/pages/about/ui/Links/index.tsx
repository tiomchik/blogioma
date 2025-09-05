import React from "react";
import "./index.scss";

const Links: React.FC = () => {
  return (
    <>
      <h1 className="links-heading">Links:</h1>
      <address className="links">
        <ul>
          <li>
            <a href="https://github.com/tiomchik/blogioma">
              Blogioma's Github repository
            </a>
          </li>
          <li>
            <a href="https://iconer.app/iconoir/">Icons source</a>
          </li>
        </ul>
      </address>
    </>
  );
};

export default Links;
