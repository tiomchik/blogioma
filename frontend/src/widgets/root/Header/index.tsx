import React, { useContext } from "react";
import { AuthContext } from "@/app/contexts";
import Logo from "./Logo";
import AddArticleButton from "./AddArticleButton";
import SearchButton from "./SearchButton";
import RandomArticleButton from "./RandomArticleButton";
import Account from "./Account";
import "./index.scss";

const Header: React.FC = () => {
  const { user } = useContext(AuthContext);

  return (
    <header className="header">
      <div className="container">
        <ul className="nav">
          <li>
            <Logo />
          </li>
          {user && (
            <li>
              <AddArticleButton />
            </li>
          )}
          <li>
            <SearchButton />
          </li>
          <li>
            <RandomArticleButton />
          </li>
          <li>
            <Account />
          </li>
        </ul>
      </div>
    </header>
  );
};

export default Header;
