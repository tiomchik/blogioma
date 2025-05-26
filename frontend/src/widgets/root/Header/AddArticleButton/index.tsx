import React from "react";
import { Link } from "@tanstack/react-router";
import AddArticleIcon from "./add-article.svg?react";
import { isOnPage } from "@/shared/utils";

const AddArticleButton: React.FC = () => {
  return (
    <Link
      to="/article/add"
      className={isOnPage("/article/add") ? "selected" : ""}
    >
      <div className="wrapper">
        <AddArticleIcon />
      </div>
      Add article
    </Link>
  );
};

export default AddArticleButton;
