import React from "react";
import { Link } from "@tanstack/react-router";
import { isOnPage } from "@/shared/utils";
import SearchIcon from "./search.svg?react";

const SearchButton: React.FC = () => {
  return (
    <Link to="/search" className={isOnPage("/search") ? "selected" : ""}>
      <div className="wrapper">
        <SearchIcon />
      </div>
      Search
    </Link>
  );
};

export default SearchButton;
