import React from "react";
import { useAuth } from "@/app/contexts";
import Logo from "./Logo";
import AddArticleButton from "./AddArticleButton";
import SearchButton from "./SearchButton";
import RandomArticleButton from "./RandomArticleButton";
import Account from "./Account";
import "./index.scss";

const Header: React.FC = () => {
  const { currentUser } = useAuth();

  return (
    <header className="header">
      <div className="container">
        <ul className="nav">
          <li>
            <Logo />
          </li>
          {currentUser && (
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
